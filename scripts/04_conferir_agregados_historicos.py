#!/usr/bin/env python3
"""Confere totais presidenciais históricos; não estimar transferências individuais."""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit

EXPECTED = {'13', '22'}

def carregar_controles(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError('Nenhum controle encontrado.')
    result = {}
    for row in rows:
        year, turn = int(row['ANO_ELEICAO']), int(row['NR_TURNO'])
        if year != 2022 or turn not in (1, 2):
            raise ValueError('Este controle cobre apenas os dois turnos de 2022.')
        code = row['IDENTIFICADOR']
        votes = int(row['QT_VOTOS_NOMINAIS'])
        total = int(row['QT_VOTOS_VALIDOS_BR'])
        if votes < 0 or total <= 0:
            raise ValueError('Contagens inválidas.')
        parsed = urlsplit(row['SOURCE_URL'])
        if parsed.scheme != 'https' or parsed.hostname != 'www.tse.jus.br':
            raise ValueError('Fonte não é domínio oficial do TSE.')
        d = result.setdefault(turn, {'total': total, 'votos': {}, 'fontes': set()})
        if d['total'] != total or code in d['votos']:
            raise ValueError('Denominadores divergentes ou registro repetido.')
        d['votos'][code] = votes
        d['fontes'].add(row['SOURCE_URL'])
    if set(result) != {1, 2}:
        raise ValueError('Dois turnos são obrigatórios.')
    for turn, d in result.items():
        if turn == 1 and set(d['votos']) != EXPECTED | {'OUTROS_AGREGADOS'}:
            raise ValueError('Faltam candidaturas ou agregado OUTROS no primeiro turno.')
        if turn == 2 and set(d['votos']) != EXPECTED:
            raise ValueError('Segundo turno deve ter dois candidatos.')
        if sum(d['votos'].values()) != d['total']:
            raise ValueError(f'Soma divergente do TSE no turno {turn}.')
    return result

def avaliar(result):
    a, b = result[1], result[2]
    diffs = {candidate: b['votos'][candidate] - a['votos'][candidate] for candidate in sorted(EXPECTED)}
    var_valid = b['total'] - a['total']
    outros = a['votos']['OUTROS_AGREGADOS']
    if sum(diffs.values()) != outros + var_valid:
        raise AssertionError('Identidade contábil de votos válidos não fecha.')
    return {
        'ano': 2022,
        'escopo': 'Presidência, Brasil inteiro, votos válidos',
        'observacao': 'Comparação descritiva; não identifica mudança de voto individual.',
        'votos_validos_primeiro_turno': a['total'],
        'votos_validos_segundo_turno': b['total'],
        'diferenca_votos_validos': var_valid,
        'outros_candidatos_primeiro_turno': outros,
        'diferencas_por_candidatura': diffs,
        'identidade_aritmetica_verificada': True,
        'fontes': sorted(a['fontes'] | b['fontes']),
        'restricao': 'Não extrapolar 2022 para 2026; não inferir manada ou transferência individual.',
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arquivo', type=Path, required=True)
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    if args.saida.exists():
        raise SystemExit('Destino existente preservado, escolha outro caminho.')
    result = avaliar(carregar_controles(args.arquivo))
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
