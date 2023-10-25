import datetime

import genshin
from rich import print


async def get_resin(cookies, uid):
    client = genshin.Client(cookies, lang="ja-jp")

    print("get resin...")
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
    print("OK")
    return regin_data
