#!/usr/bin/env python
"""
Script para auxiliar na atualização da versão do projeto no GitHub.
Este script ajuda a criar tags de versão e realizar o push para o repositório remoto.
"""

import os
import sys
import subprocess
import argparse

def run_command(command, desc=None):
    """Executa um comando shell e exibe o resultado."""
    if desc:
        print(f"\n{desc}...")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Erro ao executar comando: {command}")
        print(f"Saída de erro: {result.stderr}")
        return False, result.stdout, result.stderr
    
    if result.stdout:
        print(result.stdout)
    
    return True, result.stdout, result.stderr

def init_git_repo_if_needed():
    """Inicializa o repositório Git se necessário."""
    if not os.path.exists('.git'):
        if not run_command('git init')[0]:
            return False
    return True

def check_remote_exists():
    """Verifica se o remote origin já existe."""
    result = subprocess.run('git remote -v', shell=True, capture_output=True, text=True)
    return 'origin' in result.stdout

def get_current_branch():
    """Obtém o nome da branch atual."""
    success, stdout, stderr = run_command('git branch --show-current', "Obtendo nome da branch atual")
    if success:
        return stdout.strip()
    return None

def check_branch_exists(branch_name):
    """Verifica se uma branch específica existe."""
    success, stdout, stderr = run_command(f'git branch')
    if success:
        return branch_name in stdout
    return False

def setup_git_repo(remote_url=None, branch="main"):
    """Configura o repositório Git."""
    if not init_git_repo_if_needed():
        return False
    
    # Adicionar remote se fornecido e não existir
    if remote_url and not check_remote_exists():
        if not run_command(f'git remote add origin {remote_url}', 'Adicionando repositório remoto')[0]:
            return False
    
    # Verificar qual branch estamos
    current_branch = get_current_branch()
    
    # Se não estamos em nenhuma branch (repositório vazio ou recém-inicializado)
    if not current_branch:
        # Criar primeiro commit se necessário
        has_commits, stdout, stderr = run_command('git log -1')
        if not has_commits:
            print("\nRepositório vazio, criando commit inicial...")
            if not run_command('git add .', 'Adicionando arquivos para commit inicial')[0]:
                return False
            if not run_command('git commit -m "Commit inicial"', 'Criando commit inicial')[0]:
                return False
        
        # Criar e mudar para a branch desejada
        print(f"\nCriando branch {branch}...")
        if not run_command(f'git checkout -b {branch}', f'Criando e mudando para branch {branch}')[0]:
            return False
    elif current_branch != branch:
        # Se já estamos em uma branch diferente, verificar se a branch desejada existe
        if check_branch_exists(branch):
            # Se a branch existir, mudar para ela
            if not run_command(f'git checkout {branch}', f'Mudando para branch {branch}')[0]:
                return False
        else:
            # Se não existir, criar a partir da atual
            if not run_command(f'git checkout -b {branch}', f'Criando branch {branch}')[0]:
                return False
    
    return True

def check_tag_exists(version):
    """Verifica se uma tag já existe."""
    success, stdout, stderr = run_command(f'git tag -l v{version}')
    return success and f"v{version}" in stdout

def create_version_tag(version):
    """Cria uma tag de versão."""
    tag_name = f"v{version}"
    
    # Verifica se a tag já existe
    if check_tag_exists(version):
        print(f"\nA tag {tag_name} já existe.")
        choice = input("Deseja (s)ubstituir a tag existente, (i)ncrementar a versão ou (c)ancelar? [s/i/c]: ").lower()
        
        if choice == 'c' or choice == 'cancelar':
            print("Operação de criação de tag cancelada.")
            return False
        
        elif choice == 's' or choice == 'substituir':
            # Remove a tag existente
            run_command(f'git tag -d {tag_name}', f'Removendo tag {tag_name} existente')
            
        elif choice == 'i' or choice == 'incrementar':
            # Incrementa a versão
            parts = version.split('.')
            if len(parts) >= 3:
                parts[-1] = str(int(parts[-1]) + 1)
                new_version = '.'.join(parts)
                print(f"\nIncrementando versão para {new_version}")
                return create_version_tag(new_version)
            else:
                new_version = f"{version}.1"
                print(f"\nIncrementando versão para {new_version}")
                return create_version_tag(new_version)
        else:
            print("Opção inválida. Operação de criação de tag cancelada.")
            return False
    
    tag_msg = f"Versão {version}"
    if not run_command(f'git tag -a v{version} -m "{tag_msg}"', f'Criando tag v{version}')[0]:
        return False
    return True

def push_to_remote(branch="main", push_tags=True):
    """Envia as alterações para o repositório remoto."""
    current_branch = get_current_branch()
    if not current_branch:
        print("Não foi possível determinar a branch atual.")
        return False
    
    # Enviar branch
    if not run_command(f'git push -u origin {current_branch}', f'Enviando branch {current_branch} para o repositório remoto')[0]:
        return False
    
    # Enviar tags, se solicitado
    if push_tags:
        if not run_command('git push --tags', 'Enviando tags para o repositório remoto')[0]:
            return False
    
    return True

def update_version():
    """Função principal para atualizar a versão no repositório."""
    parser = argparse.ArgumentParser(description='Atualiza a versão do projeto no Git')
    parser.add_argument('--version', default='2.0.0', help='Número da versão (ex: 2.0.0)')
    parser.add_argument('--remote', help='URL do repositório remoto (se ainda não configurado)')
    parser.add_argument('--branch', default='main', help='Nome da branch (padrão: main)')
    parser.add_argument('--commit-msg', default='Atualização para a versão 2.0', 
                        help='Mensagem para o commit')
    
    args = parser.parse_args()
    
    print(f"=" * 70)
    print(f"Atualizando para a versão {args.version}")
    print(f"=" * 70)
    
    # Configurar repositório
    if not setup_git_repo(args.remote, args.branch):
        print("Erro ao configurar o repositório Git.")
        return False
    
    # Adicionar todos os arquivos
    if not run_command('git add .', 'Adicionando arquivos')[0]:
        return False
    
    # Fazer commit
    if not run_command(f'git commit -m "{args.commit_msg}"', 'Commitando alterações')[0]:
        return False
    
    # Criar tag de versão
    if not create_version_tag(args.version):
        return False
    
    # Perguntar se deseja enviar para o repositório remoto
    response = input("\nDeseja enviar as alterações para o repositório remoto? (s/n): ").lower()
    if response == 's' or response == 'sim':
        if not push_to_remote(args.branch, True):
            print("Erro ao enviar alterações para o repositório remoto.")
            return False
    
    print(f"\n{'-' * 70}")
    print(f"Processo de atualização para a versão {args.version} concluído com sucesso!")
    current_branch = get_current_branch() or args.branch
    print(f"Os arquivos foram commitados localmente na branch '{current_branch}' e a tag foi criada.")
    if response == 's' or response == 'sim':
        print(f"As alterações foram enviadas para o repositório remoto.")
    else:
        print(f"As alterações não foram enviadas para o repositório remoto.")
        print(f"Use 'git push -u origin {current_branch}' e 'git push --tags' quando desejar enviar.")
    print(f"{'-' * 70}")
    
    return True

if __name__ == "__main__":
    try:
        update_version()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")