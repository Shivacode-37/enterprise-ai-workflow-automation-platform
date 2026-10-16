
from collections import Counter

from sqlalchemy import func

from app.database.connection import SessionLocal
from app.models.assets import Asset
from app.models.user import User


TARGET_TOTAL = 250
SEED_PREFIX = "DEMO-SEED-"

ASSET_TYPES = ["LAPTOP", "MONITOR", "KEYBOARD", "MOUSE", "HEADSET"]

TYPE_WEIGHTS = {
    "LAPTOP": 80,
    "MONITOR": 50,
    "KEYBOARD": 45,
    "MOUSE": 45,
    "HEADSET": 30,
}

LOCATIONS = ["Bangalore", "Hyderabad", "Pune", "Gurugram", "Chennai"]

MODELS = {
    "LAPTOP": ["Business Laptop 14", "Business Laptop 15", "Developer Laptop"],
    "MONITOR": ["24-inch Monitor", "27-inch Monitor"],
    "KEYBOARD": ["Wired Keyboard", "Wireless Keyboard"],
    "MOUSE": ["Wired Mouse", "Wireless Mouse"],
    "HEADSET": ["USB Headset", "Wireless Headset"],
}


def main():
    db = SessionLocal()

    try:
        current_total = db.query(func.count(Asset.id)).scalar() or 0

        print(f"Current inventory: {current_total}")
        print(f"Target inventory: {TARGET_TOTAL}")

        if current_total > TARGET_TOTAL:
            raise RuntimeError(
                "Inventory already exceeds the target. No changes made."
            )

        if current_total == TARGET_TOTAL:
            print("Target already reached. Nothing to add.")
            return

        missing = TARGET_TOTAL - current_total

        user_ids = [
            row[0]
            for row in db.query(User.id)
            .filter(User.is_active.is_(True))
            .order_by(User.id)
            .all()
        ]

        if not user_ids:
            raise RuntimeError(
                "No active users found for assigned demo assets."
            )

        existing_serials = {
            row[0]
            for row in db.query(Asset.serial_number).all()
        }

        # Determine the next unused seed serial number.
        seed_numbers = []
        for serial in existing_serials:
            if serial.startswith(SEED_PREFIX):
                suffix = serial[len(SEED_PREFIX):]
                if suffix.isdigit():
                    seed_numbers.append(int(suffix))

        next_number = max(seed_numbers, default=0) + 1

        # Scale category counts to the number of missing records.
        weight_total = sum(TYPE_WEIGHTS.values())
        type_counts = {
            asset_type: (missing * weight) // weight_total
            for asset_type, weight in TYPE_WEIGHTS.items()
        }

        # Distribute rounding leftovers without exceeding the target.
        remainder = missing - sum(type_counts.values())
        for asset_type in ASSET_TYPES:
            if remainder == 0:
                break
            type_counts[asset_type] += 1
            remainder -= 1

        planned_types = []
        for asset_type in ASSET_TYPES:
            planned_types.extend([asset_type] * type_counts[asset_type])

        # Make 75% available, 20% assigned, 5% maintenance.
        available_count = round(missing * 0.75)
        assigned_count = round(missing * 0.20)
        maintenance_count = missing - available_count - assigned_count

        planned_statuses = (
            ["AVAILABLE"] * available_count
            + ["ASSIGNED"] * assigned_count
            + ["MAINTENANCE"] * maintenance_count
        )

        new_assets = []

        for index, (asset_type, asset_status) in enumerate(
            zip(planned_types, planned_statuses)
        ):
            serial_number = f"{SEED_PREFIX}{next_number:05d}"
            while serial_number in existing_serials:
                next_number += 1
                serial_number = f"{SEED_PREFIX}{next_number:05d}"

            existing_serials.add(serial_number)
            next_number += 1

            assigned_to = None
            if asset_status == "ASSIGNED":
                assigned_to = user_ids[index % len(user_ids)]

            model_options = MODELS[asset_type]
            name = model_options[index % len(model_options)]

            new_assets.append(
                Asset(
                    asset_type=asset_type,
                    name=name,
                    serial_number=serial_number,
                    status=asset_status,
                    location=LOCATIONS[index % len(LOCATIONS)],
                    assigned_to=assigned_to,
                )
            )

        if len(new_assets) != missing:
            raise RuntimeError("Incorrect number of assets generated.")

        # Add records inside a transaction and verify before commit.
        db.add_all(new_assets)
        db.flush()

        resulting_total = db.query(func.count(Asset.id)).scalar() or 0

        if resulting_total != TARGET_TOTAL:
            raise RuntimeError(
                f"Expected {TARGET_TOTAL} assets, found {resulting_total}. "
                "Transaction will be rolled back."
            )

        db.commit()

        print(f"\nSuccessfully added {len(new_assets)} assets.")
        print(f"Final inventory: {resulting_total}")

        print("\nNew assets by type:")
        for asset_type, count in sorted(Counter(
            asset.asset_type for asset in new_assets
        ).items()):
            print(f"  {asset_type}: {count}")

        print("\nNew assets by status:")
        for asset_status, count in sorted(Counter(
            asset.status for asset in new_assets
        ).items()):
            print(f"  {asset_status}: {count}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
