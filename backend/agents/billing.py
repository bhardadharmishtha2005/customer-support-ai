def handle_billing(message: str) -> str:
    """
    Simulates parsing user details to look up financial and invoice inquiries.
    """
    msg = message.lower()
    if "charged twice" in msg or "double charge" in msg:
        return (
            "I noticed you mentioned being charged twice. I've initiated an automated scan "
            "on your billing profile. It looks like a duplicate authorization hold occurred this month. "
            "Our system is already reversing the second charge—expect it back in your account in 3-5 business days!"
        )
    return (
        f"Thank you for contacting billing support regarding: '{message}'. "
        "I am looking at your active customer transaction logs and will resolve this payment request immediately."
    )