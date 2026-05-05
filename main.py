import requests
from deep_translator import GoogleTranslator
import os
import json
from datetime import datetime
from pathlib import Path

# Arquivo de dados
ARQUIVO_DADOS = "dados_gatos.json"

def carregar_dados():
    """Carrega dados de favoritos e histórico"""
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"favoritos": [], "historico": [], "total_visualizacoes": 0}

def salvar_dados(dados):
    """Salva dados de favoritos e histórico"""
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def adicionar_ao_historico(fato):
    """Adiciona um fato ao histórico"""
    dados = carregar_dados()
    dados["historico"].append({
        "fato": fato,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    dados["total_visualizacoes"] += 1
    salvar_dados(dados)

def adicionar_favorito(fato):
    """Adiciona um fato aos favoritos"""
    dados = carregar_dados()
    if fato not in dados["favoritos"]:
        dados["favoritos"].append(fato)
        salvar_dados(dados)
        print("⭐ Adicionado aos favoritos!")
    else:
        print("⭐ Já está nos favoritos!")

def exibir_historico():
    """Exibe o histórico de fatos"""
    dados = carregar_dados()
    if not dados["historico"]:
        print("\n📖 Nenhum fato visualizado ainda!")
        return
    
    print("\n" + "="*50)
    print("📖 HISTÓRICO DE FATOS")
    print("="*50)
    for i, item in enumerate(dados["historico"][-10:], 1):  # Últimos 10
        print(f"\n[{i}] {item['fato']}")
        print(f"   📅 {item['data']}")
    print("\n" + "="*50)

def exibir_favoritos():
    """Exibe os fatos favoritos"""
    dados = carregar_dados()
    if not dados["favoritos"]:
        print("\n⭐ Nenhum favorito salvo ainda!")
        return
    
    print("\n" + "="*50)
    print("⭐ FATOS FAVORITOS")
    print("="*50)
    for i, fato in enumerate(dados["favoritos"], 1):
        print(f"\n[{i}] {fato}")
    print("\n" + "="*50)

def exibir_estatisticas():
    """Exibe estatísticas de uso"""
    dados = carregar_dados()
    print("\n" + "="*50)
    print("📊 ESTATÍSTICAS")
    print("="*50)
    print(f"Total de visualizações: {dados['total_visualizacoes']}")
    print(f"Fatos favoritos: {len(dados['favoritos'])}")
    print(f"Histórico de fatos: {len(dados['historico'])}")
    print("="*50 + "\n")

def baixar_foto_gato():
    url_imagem = "https://cataas.com/cat"
    try:
        print(" Baixando foto do gatinho...")
        resposta = requests.get(url_imagem)
        
        # Cria a pasta se não existir
        if not os.path.exists("fotos_gatos"):
            os.makedirs("fotos_gatos")
            
        # Define o nome do arquivo
        caminho = os.path.join("fotos_gatos", "gato_atual.jpg")
        
        with open(caminho, "wb") as f:
            f.write(resposta.content)
            
        print(f" Foto salva em: {caminho}")
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")

def obter_fato():
    url = "https://catfact.ninja/fact"
    try:
        r = requests.get(url)
        fato_en = r.json()['fact']
        return GoogleTranslator(source='en', target='pt').translate(fato_en)
    except:
        return "Erro ao buscar fato."

def menu():
    while True:
        print("\n" + "="*30)
        print("    CAT EXPLORER 3.0 ")
        print("="*30)
        print("[1] Fato + Foto")
        print("[2] Ver Histórico")
        print("[3] Ver Favoritos")
        print("[4] Estatísticas")
        print("[5] Sair")
        op = input("\nEscolha uma opção: ")

        if op == '1':
            fato = obter_fato()
            print(f"\n🐾 {fato}")
            adicionar_ao_historico(fato)
            baixar_foto_gato()
            print("\n(Dica: Abra a pasta 'fotos_gatos' para ver!)")
            
            # Pergunta se quer adicionar aos favoritos
            favoritarr = input("\nAdicionar aos favoritos? (s/n): ").lower()
            if favoritarr == 's':
                adicionar_favorito(fato)
                
        elif op == '2':
            exibir_historico()
        elif op == '3':
            exibir_favoritos()
        elif op == '4':
            exibir_estatisticas()
        elif op == '5':
            print("\n👋 Até mais, gatinhos!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    menu()