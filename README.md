# Space Raiders (Asteroids) - README

## Descrição

Space Raiders é um jogo 2D estilo "Asteroids" / shoot 'em up desenvolvido em Python com Pygame como projeto universitário em equipe. O jogador controla uma nave, enfrenta ondas de inimigos, coleta power-ups (vida e bomba) e busca a maior pontuação. O jogo suporta 1 ou 2 jogadores locais, seleção de naves, efeitos visuais (estrelas de fundo, explosões em ripple) e fallback automático para sprites ausentes.

## Bibliotecas e módulos

- `pygame` — renderização, entrada do jogador, som e loop principal.
- Módulos padrão: `random`, `sys`, `os`.

## Requisitos

- Python 3.8+ recomendado
- `pygame`

## Instalação (Windows / PowerShell)

1. Abra o PowerShell e navegue até a pasta do projeto:

```powershell
cd "<Diretório da pasta>\asteroids"
```

2. (Opcional, recomendado) Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Atualize o pip e instale dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install pygame
```

## Como executar

No PowerShell (com o venv ativado ou não):

```powershell
python asteroids.py
```

## Estrutura de arquivos (esperada)

- `asteroids.py` — código fonte principal
- `ships/` — sprites das naves (opcional)
- `health/` — sprites de vida e barras (opcional)
- `powerups/` — sprites de power-ups como bomba (opcional)
- `projectiles/` — sprite do projétil (opcional)

Observação: o código contém fallbacks gráficos caso essas pastas/imagens não existam.

## Controles padrão

- Seleção de jogadores: ←/→ ou A/D para escolher entre 1 ou 2 jogadores, ENTER/ESPAÇO para confirmar
- Jogador 1: setas ← → ↑ ↓ para movimento, `SPACE` para atirar
- Jogador 2 (se ativado): `A`/`D` para mover horizontalmente, `W`/`S` para cima/baixo, `SHIFT` para atirar

## Detalhes interessantes

- Sistema de invulnerabilidade temporária após tomar dano
- Power-up de bomba que remove todos os inimigos e cria uma explosão central com efeito ripple
- Sistema de reviver parceiro quando um jogador com saúde cheia coleta um power-up de cura

## Nota sobre execução em PowerShell

Se o PowerShell bloquear a execução do script de ativação do venv por políticas de execução, rode como administrador ou execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Licença / Créditos

Este projeto foi desenvolvido como um trabalho universitário. Sinta-se livre para adaptar e melhorar para fins acadêmicos.
