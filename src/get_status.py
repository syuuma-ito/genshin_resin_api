import datetime

import genshin
from rich import print


async def get_status(cookies, uid):
    client = genshin.Client(cookies, lang="ja-jp")

    print("get status...")
    notes = await client.get_notes(uid)

    next_recover = notes.remaining_resin_recovery_time.total_seconds() % 480
    regin_data = {
        "current_resin": notes.current_resin,
        "max_resin": notes.max_resin,
        "next_recover": next_recover,
        "next_recover_str": str(datetime.timedelta(seconds=next_recover)),
        "full_recover": notes.remaining_resin_recovery_time.total_seconds(),
        "full_recover_str": str(notes.remaining_resin_recovery_time),
    }
    daily_mission = {
        "completed": notes.completed_commissions,
        "max": notes.max_commissions,
        "claimed": notes.claimed_commission_reward,
    }

    max_expeditions = notes.max_expeditions
    ongoing_expeditions = 0
    remaining_time = 0
    for expedition in notes.expeditions:
        if expedition.status == "Ongoing":
            ongoing_expeditions += 1
            if expedition.remaining_time.total_seconds() > remaining_time:
                remaining_time = expedition.remaining_time.total_seconds()

    expeditions = {
        "max": max_expeditions,
        "ongoing": ongoing_expeditions,
        "ongoing_str": f"{ongoing_expeditions}/{max_expeditions}",
        "remaining_time": remaining_time,
        "remaining_time_str": str(datetime.timedelta(seconds=remaining_time)),
    }

    realm = {
        "current": notes.current_realm_currency,
        "current_str": f"{notes.current_realm_currency}/{notes.max_realm_currency}",
        "max": notes.max_realm_currency,
        "next_recover": notes.remaining_realm_currency_recovery_time.total_seconds(),
        "next_recover_str": str(notes.remaining_realm_currency_recovery_time),
    }
    resin_discounts = {
        "remaining": notes.remaining_resin_discounts,
        "max": notes.max_resin_discounts,
    }
    result = {
        "regin_data": regin_data,
        "daily_mission": daily_mission,
        "expeditions": expeditions,
        "realm": realm,
        "resin_discounts": resin_discounts,
    }
    print("OK")
    return result
