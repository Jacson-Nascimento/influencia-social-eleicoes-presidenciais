#!/usr/bin/env python3
"""Inventário e coleta auditável de recursos públicos do portal de dados do TSE."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "brutos"
API = "https://dadosabertos.tse.jus.br/api/3/action/package_show"
DATASETS = (
    "resultados-2018", "resultados-2022", "resultados-2026",
    "resultados-2026-boletim-de-urna",
)

def obter_json(url):
    with urlopen(Request(url, headers={"User-Agent": "pesquisa-academica-tse/0.1"}), timeout=60) as response:
        return json.load(response)

def inventariar(dataset):
    if dataset not in DATASETS:
        raise ValueError("Conjunto não incluído no protocolo inicial.")
    payload = obter_json(API + "?" + urlencode({"id": dataset}))
    if payload.get("success") is not True:
        raise ValueError("Portal não confirmou o conjunto de dados.")
    return payload["result"]

def validar_url_tse(url):
    parsed = urlsplit(url)
    return (parsed.scheme == "https" and parsed.hostname and
            (parsed.hostname == "tse.jus.br" or parsed.hostname.endswith(".tse.jus.br")))

def baixar(dataset, resource, base=RAW_DIR):
    url = resource.get("url", "")
    if not validar_url_tse(url):
        raise ValueError("Recurso fora de domínio HTTPS oficial do TSE: " + url)
    rid = resource["id"]
    nome_original = Path(urlsplit(url).path).name or "recurso.bin"
    nome = rid + "__" + nome_original
    pasta = Path(base) / dataset
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / nome
    resumo = hashlib.sha256()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, dir=pasta) as tmp:
        temp = Path(tmp.name)
        try:
            with urlopen(Request(url, headers={"User-Agent": "pesquisa-academica-tse/0.1"}), timeout=180) as response:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    resumo.update(block)
                    tmp.write(block)
        except BaseException:
            temp.unlink(missing_ok=True)
            raise
    sha = resumo.hexdigest()
    if destino.exists():
        digest_existente = hashlib.sha256(destino.read_bytes()).hexdigest()
        temp.unlink(missing_ok=True)
        if digest_existente != sha:
            raise FileExistsError("Arquivo existente difere do download; preservado: " + str(destino))
    else:
        os.replace(temp, destino)
    manifesto = Path(base) / "manifesto_arquivos.csv"
    campos = ["dataset", "resource_id", "resource_name", "url", "obtido_utc", "bytes", "sha256", "arquivo_local"]
    registro = {
        "dataset": dataset,
        "resource_id": rid,
        "resource_name": resource.get("name", ""),
        "url": url,
        "obtido_utc": datetime.now(timezone.utc).isoformat(),
        "bytes": destino.stat().st_size,
        "sha256": sha,
        "arquivo_local": str(destino.relative_to(ROOT)) if destino.is_relative_to(ROOT) else str(destino),
    }
    existente = manifesto.exists()
    with manifesto.open("a", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=campos)
        if not existente:
            wr.writeheader()
        wr.writerow(registro)
    return registro

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, choices=DATASETS)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--list", action="store_true", help="apenas inventariar recursos")
    actions.add_argument("--download-id", help="ID exato do recurso validado no inventário")
    args = parser.parse_args()
    pkg = inventariar(args.dataset)
    resources = pkg.get("resources", [])
    print("Conjunto:", pkg.get("title"), "Licença:", pkg.get("license_id"))
    if args.list:
        for r in resources:
            print(json.dumps({k: r.get(k) for k in ("id", "name", "format", "url", "last_modified")}, ensure_ascii=False))
        return
    resource = next((r for r in resources if r.get("id") == args.download_id), None)
    if resource is None:
        raise SystemExit("ID do recurso não encontrado no inventário atual.")
    print(json.dumps(baixar(args.dataset, resource), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
