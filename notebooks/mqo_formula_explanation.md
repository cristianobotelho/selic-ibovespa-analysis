# 📚 Projeto de Caso Prático: Regressão IBOV vs. SELIC (MRLS)

Este documento detalha a implementação do **Modelo de Regressão Linear Simples (MRLS)** usando o Método de Mínimos Quadrados Ordinários (MQO/OLS), referenciando a teoria do livro **"Econometria Básica"** de Gujarati.

## 1. Definição e Estimação do Modelo (Capítulos 1 a 3)

O objetivo é estimar a relação entre o **IBOV ($Y_t$)** e a **SELIC Meta ($X_t$)** ao longo do tempo.

### 1.1. Modelo Básico

A forma funcional é o MRLS (Equação do MCRL - Modelo Clássico de Regressão Linear):

$$Y_t = \beta_0 + \beta_1 X_t + u_t$$

### 1.2. Estimação dos Coeficientes (MQO/OLS)

**Referência: Gujarati, Capítulos 2 e 3 (Método de Mínimos Quadrados Ordinários - MQO)**

Os coeficientes $\hat{\beta}_1$ e $\hat{\beta}_0$ são calculados para minimizar a Soma dos Quadrados dos Resíduos (SQE).

| Variável Calculada | Nome no Gujarati | Fórmula Matemática | Explicação |
| :--- | :--- | :--- | :--- |
| `Y_media`, `X_media` | Médias Amostrais | $\bar{Y}, \bar{X}$ | Base para o cálculo da variância e covariância. |
| `SXY` | Covariância Não Normalizada | $\sum (X_i - \bar{X})(Y_i - \bar{Y})$ | Mede a dispersão conjunta entre $X$ e $Y$. |
| `SXX` | Variância Não Normalizada de $X$ | $\sum (X_i - \bar{X})^2$ | Mede a dispersão de $X$ em torno de sua média. |
| **`beta_1`** | **Estimador de Inclinação** | $\hat{\beta}_1 = SXY / SXX$ | Representa o impacto marginal de $X$ sobre $Y$. |
| **`beta_0`** | **Estimador de Intercepto** | $\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}$ | Valor esperado de $Y$ quando $X=0$. |

---

## 2. Análise da Variança e Qualidade do Ajuste (Capítulo 3)

Após a estimação, avaliamos o quão bem o modelo ajusta os dados.

### 2.1. Decomposição da Variança

**Referência: Gujarati, Capítulo 3 (Medida de Qualidade do Ajuste)**

A **Soma Total dos Quadrados (SQT)** é decomposta em duas partes: a explicada pelo modelo (SQR) e a residual (SQE).

| Variável Calculada | Nome no Gujarati | Fórmula Matemática | Explicação |
| :--- | :--- | :--- | :--- |
| `u2_residuo` | Resíduo ao Quadrado | $\hat{u}_t^2 = (Y_t - \hat{Y}_t)^2$ | Componente do erro para cada observação. |
| `SQE` | Soma dos Quadrados dos Erros | $\sum \hat{u}_t^2$ | Medida da variância não explicada pelo modelo. |
| `SQT` | Soma Total dos Quadrados | $\sum (Y_t - \bar{Y})^2$ | Variância total de $Y$. |
| `SQR` | Soma dos Quadrados da Regressão | $SQR = SQT - SQE$ | Medida da variância explicada pelo modelo. |

### 2.2. Coeficiente de Determinação ($R^2$)

**Referência: Gujarati, Capítulo 3 (O Coeficiente de Determinação, $R^2$)**

O $R^2$ indica a proporção da variação total de $Y$ que é explicada por $X$.

| Variável Calculada | Fórmula Matemática | Explicação |
| :--- | :--- | :--- |
| **`R2`** | $R^2 = SQR/SQT$ | O percentual da variação do IBOV ($Y$) explicado pela SELIC ($X$). |
| **`R2_ajustado`** | $R_{ajustado}^2 = 1 - \left(1 - R^2\right) \frac{n-1}{n-2}$ | $R^2$ corrigido por graus de liberdade, mais útil em MRLM. |

---

## 3. Inferência Estatística e Testes de Hipóteses (Capítulo 5)

Os testes de hipóteses determinam se os coeficientes são estatisticamente significantes, ou seja, se são diferentes de zero.

### 3.1. Variância do Erro e dos Estimadores

**Referência: Gujarati, Capítulo 3 (Estimativa da Variância do Erro)** e **Capítulo 4 (Propriedades dos Estimadores de MQO)**

| Variável Calculada | Nome no Gujarati | Fórmula Matemática | Explicação |
| :--- | :--- | :--- | :--- |
| **`var2`** | Variância do Erro ($\hat{\sigma}^2$) | $SQE / (n-2)$ | Estimativa não viesada da variância do termo de erro ($u_t$). |
| $Var(\hat{\beta}_1)$ | Variância do Estimador $\hat{\beta}_1$ | $\hat{\sigma}^2 / SXX$ | Usada para calcular o $SE$ de $\hat{\beta}_1$. |
| $Var(\hat{\beta}_0)$ | Variância do Estimador $\hat{\beta}_0$ | $\hat{\sigma}^2 \left[ \frac{\sum X_i^2}{n \cdot SXX} \right]$ | Usada para calcular o $SE$ de $\hat{\beta}_0$. |
| $SE(\hat{\beta})$ | Erro Padrão | $\sqrt{Var(\hat{\beta})}$ | Desvio-padrão do estimador, crucial para o Teste $t$. |

### 3.2. Teste $\boldsymbol{F}$ e Teste $\boldsymbol{t}$

**Referência: Gujarati, Capítulo 5 (Teste de Hipóteses)**

| Variável Calculada | Teste | Hipótese Nula ($H_0$) | Fórmula Matemática | Explicação |
| :--- | :--- | :--- | :--- | :--- |
| **`F`** | Estatística $F$ | $\beta_1 = 0$ | $\frac{SQR/1}{SQE/(n-2)}$ | Testa a significância **geral** do modelo. |
| **`t_beta_1`** | Estatística $t$ | $\beta_1 = 0$ | $\hat{\beta}_1 / SE(\hat{\beta}_1)$ | Testa a significância **individual** de $\hat{\beta}_1$. |
| **`t_beta_0`** | Estatística $t$ | $\beta_0 = 0$ | $\hat{\beta}_0 / SE(\hat{\beta}_0)$ | Testa a significância **individual** de $\hat{\beta}_0$. |


## 🧐 O Significado do Teste $F$ (Gujarati, Capítulo 5)

O Teste $F$ é um **Teste de Significância Global** do modelo.

#### 3.2.1. Hipótese Testada

O Teste $F$ avalia se **pelo menos uma** das variáveis explicativas ($X$) tem um poder de explicação estatisticamente significativo sobre a variável dependente ($Y$).

* **Hipótese Nula ($H_0$):** Todos os coeficientes de inclinação são **zero**.
    * No seu MRLS (apenas $\hat{\beta}_1$): $H_0: \beta_1 = 0$.
* **Hipótese Alternativa ($H_A$):** Pelo menos um coeficiente de inclinação é **diferente de zero**.
    * No seu MRLS: $H_A: \beta_1 \neq 0$.

Se você **rejeitar $H_0$**, isso significa que o seu modelo, como um todo, é estatisticamente útil e que a variável SELIC ($X$) é relevante na explicação do IBOV ($Y$).

#### 3.2.2. A Intuição da Estatística $F$

A Estatística $F$ compara a variância **explicada** pelo modelo (SQR) com a variância **não explicada** (SQE):

$$F = \frac{\text{SQR} / \text{g.l. da Regressão}}{\text{SQE} / \text{g.l. do Erro}} = \frac{\text{Média Quadrática da Regressão (MQR)}}{\text{Média Quadrática do Erro (MQE)}}$$

* Se o modelo **não tem poder de explicação**, SQR é pequeno, SQE é grande, e $F \approx 1$.
* Se o modelo **tem bom poder de explicação**, SQR é grande, SQE é pequeno, e $F$ é **muito maior que 1**.

#### 3.2.3. Interpretação do seu Resultado: $F = 16.808962$

Para interpretar o valor $F$, precisamos compará-lo com o **Valor Crítico** da distribuição $F$, usando os graus de liberdade (g.l.) da sua regressão ($k-1 = 1$) e do erro ($n-k$).

| Nível de Significância ($\alpha$) | Valor Crítico (g.l. 1 e 180-200, aprox.) |
| :--- | :--- |
| **5%** | $\approx 3.84$ |
| **1%** | $\approx 6.63$ |

**Conclusão:**

valor $F = 16.808962$ é **muito maior** que o valor crítico de 6.63 (para 1% de significância).

Isso significa que você **rejeita categoricamente a Hipótese Nula ($H_0: \beta_1 = 0$)**.

Em termos práticos: **O modelo de regressão é estatisticamente significativo** e a variável SELIC Meta ($X$) tem um impacto estatisticamente relevante na variação do IBOV ($Y$) no período de 2009 a 2024.

---

## 4. Diagnóstico de Heterocedasticidade (Capítulo 11)

Em modelos com dados financeiros (como IBOV), um pressuposto crucial do MCRL (variância constante dos erros) é frequentemente violado, caracterizando a **Heterocedasticidade**. Se isso ocorrer, o $SE$ e os testes $t$ do Passo 3 são viesados, mas os coeficientes $\hat{\beta}_0$ e $\hat{\beta}_1$ permanecem não viesados.

### 4.1. Teste $\boldsymbol{t}$ Robusto (Huber-White)

**Referência: Gujarati, Capítulo 11 (Métodos para Obter Erros Padrão Robustos)**

Para obter inferência válida sob heterocedasticidade, utilizamos o Erro Padrão Robusto (Heteroskedasticity Consistent Standard Errors - HCSE).

| Variável Calculada | Nome | Fórmula Matemática (Simplificada) | Explicação |
| :--- | :--- | :--- | :--- |
| `Sum_u2_Xc2` | Soma de $\hat{u}^2 \cdot \tilde{X}^2$ | $\sum (X_i - \bar{X})^2 \cdot \hat{u}_i^2$ | Componente central para a fórmula de variância robusta. |
| $SE_{Robusto}(\hat{\beta}_1)$ | Erro Padrão Robusto | $\sqrt{\frac{\sum \tilde{X}_i^2 \hat{u}_i^2}{SXX^2}}$ | Erro Padrão válido mesmo com heterocedasticidade. |
| **`t_Robusto_beta_1`** | Estatística $t$ Robusta | $\hat{\beta}_1 / SE_{Robusto}(\hat{\beta}_1)$ | Teste de significância **válido** sob heterocedasticidade. |

---

Com esta organização, você tem tanto o código quanto a fundamentação teórica clara para o seu projeto!

Gostaria que eu montasse o código Polars/SQL para um teste formal de heterocedasticidade, como o **Teste de Breusch-Pagan** ou **Teste de White**, que são detalhados no Capítulo 11 do Gujarati?