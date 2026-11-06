# PROJECT_BIBLE — FIXTURE FICTÍCIO "A Porta do Relojoeiro" (apenas para teste)

## 3. Continuidade narrativa
- P1: Pip encontra a porta da oficina; público escolheu ENTRAR; porta trancou atrás; lanterna quebrou; pata esquerda queimada.

## Canon
```canon
# visual
style.render = 2D recortado, contorno grosso, textura de papel
style.palette = ambar #E8A33D, azul-noite #1B2A41, verde-musgo #6B8F4E
# personagens
char.pip.appearance = criatura pequena verde-musgo, cabeça grande, orelhas longas
char.pip.outfit = cachecol azul
char.pip.proportion = cabeca 1/2 do corpo
char.pip.voice = aguda e suave, fala rapida, gagueja "eh" quando nervoso
char.pip.accent = neutro
char.pip.mannerism = orelha estremece quando assustado
char.pip.state.left_paw = queimada, enfaixada com tira de pano
char.pip.location = dentro da oficina da torre
char.corvo.appearance = corvo grande, penas cinza, monóculo dourado
char.corvo.outfit = nenhuma
char.corvo.voice = grave, lenta, rouca
char.corvo.accent = nordestino
char.corvo.mannerism = bate o bico duas vezes antes de falar
# cenário e objetos
scene.main = oficina de relojoeiro na torre do relogio, noite, chuva
scene.light = lampiao ambar fraco, sombras longas
obj.brass_key = chave de latao com tres dentes, no bolso do cachecol de pip
obj.lantern = quebrada, vidro rachado, apagada
obj.door = trancada por fora, sem retorno a rua
# decisão do público
choice.p1 = entrar (vencedor); alternativa fugir não explorada
# técnico
tech.fps = 24
tech.fps = 30
tech.resolution = 1080x1920
tech.camera = push-in lento, sem tremor
tech.motion = squash-and-stretch leve, easing ease-in-out
```
