"""
Toy Story 2 — custom Archipelago client launcher.

The ONLY behavioural difference from the generic "BizHawk Client" is that this
hides the on-screen "Sent" line for items you send to YOURSELF (sender ==
receiver == you), which otherwise appears redundantly next to the matching
"Received" line.

Implementation note: rather than reimplement the BizHawk client's connection /
watcher loop (whose internals vary across Archipelago versions), this installs a
small wrapper around BizHawkClientContext.on_print_json and then calls the stock,
public `launch` entry point. All of the real game integration still lives in
ts2_client.py (`ToyStory2Client(BizHawkClient)`), which the BizHawk context
auto-discovers and attaches exactly as before.
"""
from __future__ import annotations


def _install_self_send_filter() -> None:
    """Wrap BizHawkClientContext.on_print_json to drop self->self item sends.

    Idempotent: safe to call more than once (won't stack wrappers).
    """
    from worlds._bizhawk.context import BizHawkClientContext

    if getattr(BizHawkClientContext, "_ts2_selfsend_filter", False):
        return

    _orig_on_print_json = BizHawkClientContext.on_print_json

    def on_print_json(self, args: dict) -> None:
        # Suppress the redundant "Sent" line for an item you send to yourself: an
        # ItemSend whose receiving slot AND item-source slot are both this player.
        # Everything else (other players' sends, your sends to others, your own
        # received items, chat, hints, etc.) renders normally.
        try:
            if args.get("type", "") == "ItemSend":
                receiving = args.get("receiving")
                item = args.get("item")
                sender = getattr(item, "player", None)
                if (receiving is not None and sender is not None
                        and self.slot_concerns_self(receiving)
                        and self.slot_concerns_self(sender)):
                    return
        except Exception:
            # Never let the filter break message handling.
            pass
        return _orig_on_print_json(self, args)

    BizHawkClientContext.on_print_json = on_print_json
    BizHawkClientContext._ts2_selfsend_filter = True


def launch(*args: str) -> None:
    """Launcher-component entry point.

    Installs the self-send filter, then defers to the stock BizHawk client's
    public launch entry so the connection/watcher behaviour is identical to the
    generic client.
    """
    _install_self_send_filter()
    from worlds._bizhawk.context import launch as bizhawk_launch
    bizhawk_launch(*args)