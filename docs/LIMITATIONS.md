# Limitações Conhecidas - v1.0

## Canonicalização de Goals

### Status: Limitação Aceita para v1.0

**Descrição:**

Goals podem apresentar pontos auxiliares na notação final, por exemplo:
- `"Provar: ∠MBC = ∠MCB"` em vez do formato canônico `"Provar: ∠ABC = ∠ACB"`

**Por que isso acontece:**

1. O DDAR deduz fatos simbólicos corretamente, mas não "sabe" qual é o triângulo principal
2. A canonicalização atual detecta pontos auxiliares, mas não mapeia automaticamente ângulos auxiliares → ângulos principais
3. Isso é conhecimento semântico/geométrico externo ao motor lógico

**Impacto:**

- ✅ Lógica: Correto
- ✅ Dedução: Automática
- ⚠️ Pedagogia: Notação pode não ser ideal para ensino humano direto
- ✅ Dataset/LLM: Utilizável (LLMs aprendem o mapeamento)

**Solução Futura (pós-v1):**

Canonicalização completa requer:
- Identificação explícita do triângulo principal do problema
- Mapeamento geométrico: pontos auxiliares colineares → vértices principais
- Heurísticas para substituição segura de ângulos

**Decisão:**

Aceito como limitação conhecida para v1.0. O sistema está pronto para geração em lote. Canonicalização perfeita pode ser implementada após análise estatística de 1k-10k exemplos.

---

*Documentação criada em: 2024*

