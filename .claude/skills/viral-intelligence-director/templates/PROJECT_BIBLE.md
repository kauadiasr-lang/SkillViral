# PROJECT_BIBLE — <título>
_Fonte única de continuidade narrativa/visual/técnica. Fatos vivem SÓ no bloco canon (um lugar, sem duplicar em outras seções ou arquivos)._
Partes concluídas: <n> · Última atualização: <data>

## Regras de edição
- Ler: bloco canon inteiro + última entrada do Part log. Não reler o resto.
- Escrever: alterar apenas as chaves que mudaram; registrar a causa no Part log. Nunca reescrever o arquivo.
- Chaves `*.voice|accent|proportion|appearance|personality`, `style.*`, `tech.*` só mudam com autorização do usuário (`~ user-approved`). Demais mudanças exigem causa narrativa (`~ narrative: <evento>`).
- Convenção de chaves: `char.<nome>.<atributo>` · `char.<nome>.state.<parte>` (ferimentos, carga) · `char.<nome>.location` · `obj.<nome>` · `scene.<nome>` · `choice.p<N>` · `style.*` · `tech.*`. Valores curtos e específicos (cores em hex, números).
- Verificação: `python3 scripts/vid.py continuity PROJECT_BIBLE.md <manifesto_da_parte>.md [--scope char.pip]`

## Canon
```canon
# visual
style.render =
style.palette =
style.lighting =
style.camera =
# personagens (repetir por personagem)
char.<nome>.appearance =
char.<nome>.outfit =
char.<nome>.proportion =
char.<nome>.personality =
char.<nome>.voice =
char.<nome>.accent =
char.<nome>.mannerism =
char.<nome>.state.<parte> =
char.<nome>.location =
# cenário e objetos
scene.main =
obj.<nome> =
# imagens de referência (verificação visual: references/visual-verification.md)
ref.<nome> =
ref.scene.<nome> =
ref.obj.<nome> =
# decisões do público (resultado + consequência concreta)
choice.p1 =
# técnico (valores travados)
tech.fps =
tech.resolution =
tech.camera =
tech.motion =
tech.audio =
```

## Part log (append-only, ≤5 linhas por parte)
- P1: <eventos> · escolha do público: <opção, nº de votos se verificado> · chaves alteradas: <lista>

## Pendências narrativas / próximos possíveis
-

## Contradições detectadas (abertas)
- (nenhuma)
