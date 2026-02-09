# Flappy Bird com Controle por Câmera

Este projeto implementa o jogo **Flappy Bird** em Python usando **Pygame**, com um diferencial: o jogador pode controlar o pulo do pássaro usando **gestos das mãos detectados pela câmera** via **OpenCV**.

Quando ambas as mãos são detectadas nas áreas definidas da câmera, o sistema simula o pressionamento da tecla **ESPAÇO**, fazendo o pássaro pular no jogo.


---

## 🎮 Funcionalidades

### flappy.py
- Implementa o jogo Flappy Bird completo.
- Inclui:
  - Física do pássaro (gravidade e pulo).
  - Geração aleatória de canos.
  - Sistema de pontuação.
  - Detecção de colisões com canos e chão.
  - Tela de **Game Over** com reinício ao pressionar **ESPAÇO**.

### camera.py
- Captura vídeo da webcam.
- Detecta presença de mãos em duas áreas da tela.
- Quando ambas as áreas estão ativas:
  - Envia a tecla **ESPAÇO** ao sistema usando `xdotool`.
  - Exibe a mensagem “Jump” na tela da câmera.

---

## 🧰 Requisitos

### Sistema
- Linux (necessário para o `xdotool`)
- Webcam funcional

### Dependências Python
```bash
pip install pygame opencv-python numpy
```

### Dependência do sistema
```bash
sudo apt install xdotool
```

---

## ▶️ Como Executar

### 1️⃣ Inicie o jogo:
```bash
python flappy.py
```

### 2️⃣ Em outro terminal, inicie o controle por câmera:
```bash
python camera.py
```

---
## 🧠 Lógica de Controle por Gestos

- Duas regiões da tela são monitoradas:
    - Lado esquerdo
    - Lado direito

- Se ambas detectarem tons de pele:
    - Um comando space é enviado ao sistema.

- Um bloqueio evita múltiplos disparos contínuos.

--- 

## 📸 Observações Importantes
- Iluminação adequada melhora bastante a detecção.

- Ajuste os valores HSV em camera.py se necessário para seu ambiente.

- O projeto foi pensado para uso educacional, demonstrações e prototipagem de interfaces alternativas.