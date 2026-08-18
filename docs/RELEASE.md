Publicar GuardianPy Community
Release local
bash
python -m pytest -q
python -m pip install build
python -m build
Release GitHub
Crea tag:
bash
git tag v0.2.0
git push origin v0.2.0
En Windows, genera dist\\GuardianPyCommunity.exe.
Adjunta a GitHub Releases:
GuardianPyCommunity.exe
GuardianPyCommunitySetup.exe si compilaste Inno Setup
GuardianPy\_mvp.zip

