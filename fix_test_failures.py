from pathlib import Path

# Fix test_main.py to ensure Authorization header is present
test_main_path = Path("tests/test_main.py")
if test_main_path.exists():
    content = test_main_path.read_text(encoding="utf-8")
    if "Authorization" not in content:
        content = content.replace("HEADERS =", 'HEADERS = {"Authorization": "Bearer test-key"}  # 🛠 Injected\n')
        test_main_path.write_text(content, encoding="utf-8")
        print("✅ Fixed: Authorization header added to test_main.py")
    else:
        print("⏭️ Authorization header already present in test_main.py")
else:
    print("❌ tests/test_main.py not found")

# Fix main.py to register routes correctly
main_py_path = Path("lifeos/main.py")
if main_py_path.exists():
    content = main_py_path.read_text(encoding="utf-8")
    updated = False

    if "from lifeos.routes.healthz" not in content:
        content = content.replace(
            "from fastapi import FastAPI",
            "from fastapi import FastAPI\nfrom fastapi.staticfiles import StaticFiles\n"
            "from lifeos.routes.healthz import router as healthz_router\n"
            "from lifeos.routes.memory import router as memory_router\n"
            "from lifeos.routes.ask import router as ask_router\n"
            "from lifeos.routes.route import router as route_router"
        )
        updated = True

    if "app.include_router(healthz_router" not in content:
        content += (
            "\n\n# ✅ Mount well-known and register routes\n"
            "app.mount(\"/.well-known\", StaticFiles(directory=\".well-known\"), name=\"well-known\")\n"
            "app.include_router(healthz_router)\n"
            "app.include_router(memory_router)\n"
            "app.include_router(ask_router)\n"
            "app.include_router(route_router)\n"
        )
        updated = True

    if updated:
        main_py_path.write_text(content, encoding="utf-8")
        print("✅ Fixed: Routes registered in lifeos/main.py")
    else:
        print("⏭️ Routes already registered in lifeos/main.py")
else:
    print("❌ lifeos/main.py not found")

# Fix memory_manager.py datetime warning (optional)
mm_path = Path("lifeos/storage/memory_manager.py")
if mm_path.exists():
    content = mm_path.read_text(encoding="utf-8")
    if "datetime.utcnow()" in content:
        content = content.replace(
            "datetime.utcnow()",
            "datetime.now(datetime.UTC)  # ⏰ Updated to timezone-aware UTC"
        )
        mm_path.write_text(content, encoding="utf-8")
        print("✅ Fixed: UTC deprecation warning in memory_manager.py")
    else:
        print("⏭️ UTC call already fixed in memory_manager.py")
else:
    print("❌ memory_manager.py not found")
