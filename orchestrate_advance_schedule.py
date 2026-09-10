"""
Master Advance Carousel Orchestrator for @ai.agent_jayant
=========================================================
Schedules carousels 2 days ahead directly into the Buffer Calendar:
- Workflow 1: 3D Tactile Architecture (slots 1 & 3)
- Workflow 2: AI Visual Studio Art (slots 2 & 4)

Daily Slots (IST / UTC):
- Slot 1 (Workflow 1): 10:00 AM IST (04:30 UTC)
- Slot 2 (Workflow 2): 01:30 PM IST (08:00 UTC)
- Slot 3 (Workflow 1): 06:00 PM IST (12:30 UTC)
- Slot 4 (Workflow 2): 09:00 PM IST (15:30 UTC)
"""

import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Slot Definitions in IST (hour, minute, workflow_type, label)
SLOT_CONFIG = [
    {
        "slot": 1,
        "workflow": "tactile",
        "ist_hour": 10,
        "ist_minute": 0,
        "label": "Morning Architectural Blueprint"
    },
    {
        "slot": 2,
        "workflow": "visual",
        "ist_hour": 13,
        "ist_minute": 30,
        "label": "Afternoon AI Visual Breakthrough"
    },
    {
        "slot": 3,
        "workflow": "tactile",
        "ist_hour": 18,
        "ist_minute": 0,
        "label": "Evening Deep Dive Architecture"
    },
    {
        "slot": 4,
        "workflow": "visual",
        "ist_hour": 21,
        "ist_minute": 0,
        "label": "Night Visual AI Showcase"
    }
]

IST_OFFSET = timedelta(hours=5, minutes=30)


def calculate_slot_utc(day_offset: int, ist_hour: int, ist_minute: int) -> str:
    """Calculates the exact UTC ISO-8601 string for a target date & IST time."""
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc + IST_OFFSET
    target_date_ist = (now_ist + timedelta(days=day_offset)).date()
    target_dt_ist = datetime(
        target_date_ist.year,
        target_date_ist.month,
        target_date_ist.day,
        ist_hour,
        ist_minute,
        0,
        tzinfo=timezone(IST_OFFSET)
    )
    target_dt_utc = target_dt_ist.astimezone(timezone.utc)
    return target_dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def run_slot(day_offset: int, slot_info: dict, dry_run: bool = False):
    slot_num = slot_info["slot"]
    workflow = slot_info["workflow"]
    label = slot_info["label"]
    iso_time = calculate_slot_utc(day_offset, slot_info["ist_hour"], slot_info["ist_minute"])

    now_ist = datetime.now(timezone.utc) + IST_OFFSET
    target_date = (now_ist + timedelta(days=day_offset)).strftime("%A, %b %d, %Y")
    ist_time_str = f"{slot_info['ist_hour']:02d}:{slot_info['ist_minute']:02d} IST"

    print("\n" + "=" * 60)
    print(f"🗓️  SCHEDULING FOR: {target_date} @ {ist_time_str} ({iso_time})")
    print(f"📌  Slot {slot_num}: {label} [{workflow.upper()} WORKFLOW]")
    print("=" * 60)

    if workflow == "tactile":
        import daily_auto_carousel
        daily_auto_carousel.run_daily_job(
            mode="customScheduled",
            dry_run=dry_run,
            draft=False,
            schedule_time=iso_time
        )
    elif workflow == "visual":
        import daily_ai_visual_carousel
        daily_ai_visual_carousel.run_visual_pipeline(
            mode="customScheduled",
            dry_run=dry_run,
            draft=False,
            schedule_time=iso_time
        )
    else:
        raise ValueError(f"Unknown workflow: {workflow}")


def main():
    parser = argparse.ArgumentParser(description="Master Advance Carousel Scheduler for @ai.agent_jayant")
    parser.add_argument("--init-2days", action="store_true", help="Generate & schedule all 4 slots for Tomorrow AND Day After Tomorrow (8 total)")
    parser.add_argument("--daily-roll", action="store_true", help="Generate & schedule all 4 slots for Day + 2 (keeps 2-day queue filled)")
    parser.add_argument("--day-offset", type=int, default=None, help="Generate for specific day offset (e.g. 1 for tomorrow, 2 for day after)")
    parser.add_argument("--slot", type=int, choices=[1, 2, 3, 4], default=None, help="Generate only a specific slot (1, 2, 3, or 4)")
    parser.add_argument("--dry-run", action="store_true", help="Generate content and render slides locally without uploading to Buffer")
    args = parser.parse_args()

    if args.slot and args.day_offset is not None:
        slot_conf = next(s for s in SLOT_CONFIG if s["slot"] == args.slot)
        run_slot(args.day_offset, slot_conf, dry_run=args.dry_run)
    elif args.init_2days:
        print("\n🚀 INITIALIZING 2 DAYS AHEAD BUFFER QUEUE...")
        # Day + 1 (Tomorrow)
        for slot in SLOT_CONFIG:
            run_slot(day_offset=1, slot_info=slot, dry_run=args.dry_run)
        # Day + 2 (Day After Tomorrow)
        for slot in SLOT_CONFIG:
            run_slot(day_offset=2, slot_info=slot, dry_run=args.dry_run)
        print("\n🎉 Both Tomorrow and Day After Tomorrow have been scheduled on Buffer!")
    elif args.daily_roll:
        print("\n🔄 RUNNING DAILY ROLLING ADVANCE SCHEDULER (DAY + 2)...")
        for slot in SLOT_CONFIG:
            run_slot(day_offset=2, slot_info=slot, dry_run=args.dry_run)
        print("\n🎉 Day + 2 has been scheduled on Buffer!")
    elif args.day_offset is not None:
        for slot in SLOT_CONFIG:
            run_slot(day_offset=args.day_offset, slot_info=slot, dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
