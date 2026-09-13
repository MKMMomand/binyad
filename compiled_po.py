"""
Compile every .po file in locale/ to .mo, forcing UTF-8.

Works without GNU gettext.
"""
import pathlib
import polib

base = pathlib.Path(__file__).parent / "locale"

count = 0
for po_path in base.rglob("*.po"):
    try:
        po = polib.pofile(
            str(po_path),
            encoding="utf-8",           # force UTF-8 read
        )

        # Ensure the header exists and declares UTF-8
        if "Content-Type" not in po.metadata:
            po.metadata["Content-Type"] = "text/plain; charset=UTF-8"
        if "MIME-Version" not in po.metadata:
            po.metadata["MIME-Version"] = "1.0"
        if "Content-Transfer-Encoding" not in po.metadata:
            po.metadata["Content-Transfer-Encoding"] = "8bit"

        mo_path = po_path.with_suffix(".mo")
        po.save_as_mofile(
            str(mo_path),
            encoding="utf-8",           # force UTF-8 write
        )
        print(f"✓ {po_path}  ->  {mo_path}")
        count += 1

    except Exception as e:
        print(f"✗ {po_path}: {e}")

print(f"\nCompiled {count} file(s).")