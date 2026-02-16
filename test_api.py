#!/usr/bin/env python3
"""
Script de teste para a API Docker
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_json(data):
    """Imprime JSON formatado"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_health():
    """Testa o endpoint de health check"""
    print("\n" + "="*50)
    print("🏥 Testando Health Check")
    print("="*50)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print_json(response.json())

def test_list_running_containers():
    """Lista apenas containers em execução"""
    print("\n" + "="*50)
    print("🐳 Listando Containers em Execução")
    print("="*50)
    response = requests.get(f"{BASE_URL}/api/v1/containers")
    print(f"Status Code: {response.status_code}")
    containers = response.json()
    print(f"Total de containers em execução: {len(containers)}")
    print_json(containers)

def test_list_all_containers():
    """Lista todos os containers (incluindo parados)"""
    print("\n" + "="*50)
    print("📦 Listando Todos os Containers")
    print("="*50)
    response = requests.get(f"{BASE_URL}/api/v1/containers?all=true")
    print(f"Status Code: {response.status_code}")
    containers = response.json()
    print(f"Total de containers: {len(containers)}")
    print_json(containers)

def test_get_container_details(container_id):
    """Obtém detalhes de um container específico"""
    print("\n" + "="*50)
    print(f"🔍 Detalhes do Container: {container_id}")
    print("="*50)
    response = requests.get(f"{BASE_URL}/api/v1/containers/{container_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(f"Erro: {response.text}")

if __name__ == "__main__":
    print("\n" + "🚀 Iniciando testes da API Docker" + "\n")
    
    try:
        # Testa health check
        test_health()
        
        # Lista containers em execução
        test_list_running_containers()
        
        # Lista todos os containers
        test_list_all_containers()
        
        # Se houver containers, testa detalhes do primeiro
        response = requests.get(f"{BASE_URL}/api/v1/containers")
        containers = response.json()
        if containers:
            first_container = containers[0]
            test_get_container_details(first_container['id'])
        
        print("\n" + "✅ Todos os testes concluídos!" + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API")
        print("Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
