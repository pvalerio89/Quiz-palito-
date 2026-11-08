"""Gera um vídeo ou Short do Quiz Palito usando os scripts que já existem na pasta dele.

Uso: py -3 automacao/gerar.py <pasta> [--previa]
  ex.: py -3 automacao/gerar.py videos/06-quiz-brasil
       py -3 automacao/gerar.py shorts/brasil-1 --previa

Ordem: gerar_vozes.py (só as falas que faltam) -> build_*.py -> gerar_kit.py.
Não muda nenhum script de vídeo: só chama cada um, como é feito no PC.
No fim copia o resultado para saida/<pasta>/ (mp4, kit do YouTube, texto do TikTok, prévia).
"""
import glob, json, os, re, shutil, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, pasta_rel, slug

# Fontes do Windows usadas pelo padrão visual atual, com o hash das versões do PC do Patrick (2026-11-03).
FONTES = {
    "seguibl.ttf": "bdf29c9b7484c631f19d6ef436a63d15f8a1a82bc856f1a0f6906c41a097d2b1",
    "segoeuib.ttf": "b169e636719880976a97e94e3b1cb3dbe5f4a38eabc037bf9f2a9165154c3ad2",
    "seguiemj.ttf": "451df9bb5546055af625ff86aa72695df43e8e170b4c6c1316fe44e9c7a22f7c",
}
BUILDS = ["build_short.py", "build_brasil.py", "build_naodiga.py", "build_prefere.py",
          "build_bandeiras.py", "build_futebol.py", "build_estados.py"]


def aviso(msg):
    # No GitHub vira um aviso amarelo no resumo da execução.
    print(f"::warning::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"AVISO: {msg}", flush=True)


def checar_fontes():
    from comum import sha256
    pasta = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
    for nome, h in FONTES.items():
        p = os.path.join(pasta, nome)
        if not os.path.exists(p):
            sys.exit(f"ERRO: fonte {nome} não existe nesta máquina. Use windows-latest.")
        if sha256(p) != h:
            aviso(f"{nome} é de outra versão que a do seu PC; confira a prévia (emojis/letras podem mudar).")


def rodar(script, *args, cwd):
    print(f"\n>>> {script} {' '.join(args)}", flush=True)
    t = time.time()
    r = subprocess.run([sys.executable, script, *args], cwd=cwd)
    if r.returncode:
        sys.exit(f"ERRO: {script} terminou com código {r.returncode}")
    print(f"<<< {script} ok ({time.time() - t:.0f}s)", flush=True)


def volume(mp4):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp4, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    if not m:
        aviso("não consegui medir o volume")
        return None
    v = float(m.group(1))
    print(f"Volume médio: {v:.1f} dB (alvo ~-26 dB)")
    if not -30 <= v <= -22:
        aviso(f"volume médio {v:.1f} dB fora do padrão (~-26 dB)")
    return v


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pasta = pasta_rel(sys.argv[1])
    previa = "--previa" in sys.argv
    aqui = os.path.join(RAIZ, pasta)
    builds = [b for b in BUILDS if os.path.exists(os.path.join(aqui, b))]
    if not builds:  # vídeo novo com outro nome de script (ex.: build_cartao.py)
        builds = sorted(os.path.basename(b) for b in glob.glob(os.path.join(aqui, "build_*.py")))
    if len(builds) != 1:
        sys.exit(f"ERRO: esperava um script de montagem em {pasta}, achei {builds or 'nenhum'}.")
    build = builds[0]
    if os.name == "nt":
        checar_fontes()

    inicio = time.time()
    antes = {p: os.path.getmtime(p) for p in glob.glob(os.path.join(aqui, "*.mp4"))}
    if os.path.exists(os.path.join(aqui, "gerar_vozes.py")):
        rodar("gerar_vozes.py", cwd=aqui)  # sem --tudo: só cria as falas que faltam
    rodar(build, *(["--previa"] if previa else []), cwd=aqui)

    saida = os.path.join(RAIZ, "saida", slug(pasta))
    shutil.rmtree(saida, ignore_errors=True)
    os.makedirs(saida)
    info = {"pasta": pasta, "modo": "previa" if previa else "completo", "build": build}

    if previa:
        for jpg in glob.glob(os.path.join(aqui, "previa", "*.jpg")):
            shutil.copy2(jpg, saida)
    else:
        if os.path.exists(os.path.join(aqui, "gerar_kit.py")):
            rodar("gerar_kit.py", cwd=aqui)
        novos = [p for p in glob.glob(os.path.join(aqui, "*.mp4")) if os.path.getmtime(p) != antes.get(p)]
        if len(novos) != 1:
            sys.exit(f"ERRO: esperava 1 mp4 novo em {pasta}, achei {len(novos)}.")
        mp4 = novos[0]
        shutil.copy2(mp4, saida)
        info["mp4"] = os.path.basename(mp4)
        info["volume_db"] = volume(mp4)
        if os.path.isdir(os.path.join(aqui, "youtube")):
            shutil.copytree(os.path.join(aqui, "youtube"), os.path.join(saida, "youtube"))
        for extra in ("tempos.json", "textos.json"):
            if os.path.exists(os.path.join(aqui, extra)):
                shutil.copy2(os.path.join(aqui, extra), saida)
    info["tempo_s"] = round(time.time() - inicio)
    json.dump(info, open(os.path.join(saida, "info.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nOK {pasta} -> saida/{slug(pasta)} ({info['tempo_s']}s)")


if __name__ == "__main__":
    main()
