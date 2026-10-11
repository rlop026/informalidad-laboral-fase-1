"""Funciones auxiliares de la Fase 2 (inferencia). Sin estado global: todo es reproducible con semilla."""
import math
import numpy as np
import pandas as pd
from scipy import stats


def p_fmt(p):
    """Formatea valores p para tablas."""
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "—"
    if p < 1e-300:
        return "< 1e-300"
    if p < 0.001:
        return f"{p:.1e}"
    return f"{p:.3f}"


def v_cramer_tabla(ct):
    """V de Cramér, chi2, gl, valor p y esperados a partir de una tabla de contingencia."""
    ct = np.asarray(ct, dtype=float)
    chi2, p, dof, esp = stats.chi2_contingency(ct, correction=False)
    n = ct.sum()
    k = min(ct.shape) - 1
    return math.sqrt(chi2 / (n * k)), chi2, dof, p, esp


def v_cramer_codigos(cod, y, ncod, ny=2):
    """V de Cramér rápida con códigos enteros 0..ncod-1 y y en {0,1} (usada en el bootstrap)."""
    tab = np.bincount(cod * ny + y, minlength=ncod * ny).reshape(ncod, ny).astype(float)
    tab = tab[tab.sum(axis=1) > 0]
    n = tab.sum()
    esp = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / n
    chi2 = ((tab - esp) ** 2 / esp).sum()
    return math.sqrt(chi2 / (n * (min(tab.shape) - 1)))


def cohen_h(p1, p2):
    """Tamaño del efecto h de Cohen para dos proporciones."""
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def woolf_or(a, b, c, d, alpha=0.05):
    """OR con IC de Woolf. Tabla [[a, b], [c, d]]: OR = (a/b)/(c/d)."""
    or_ = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    z = stats.norm.ppf(1 - alpha / 2)
    return or_, math.exp(math.log(or_) - z * se), math.exp(math.log(or_) + z * se)


def mwu_con_z(x, y, alternative="two-sided"):
    """Mann-Whitney con estadístico z (corrección por empates), rango-biserial y prob. de superioridad."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n1, n2 = len(x), len(y)
    res = stats.mannwhitneyu(x, y, alternative=alternative, method="asymptotic")
    u = res.statistic
    n = n1 + n2
    _, cuentas = np.unique(np.concatenate([x, y]), return_counts=True)
    sigma = math.sqrt(n1 * n2 / 12 * ((n + 1) - (cuentas ** 3 - cuentas).sum() / (n * (n - 1))))
    z = (u - n1 * n2 / 2) / sigma
    return {"U": u, "z": z, "p": res.pvalue, "rank_biserial": 2 * u / (n1 * n2) - 1,
            "prob_superioridad": u / (n1 * n2), "n1": n1, "n2": n2}


def trend_cochran_armitage(x_eventos, n_total, scores):
    """Prueba de tendencia de Cochran-Armitage (bilateral). Devuelve z y p."""
    x = np.asarray(x_eventos, float)
    n = np.asarray(n_total, float)
    s = np.asarray(scores, float)
    N = n.sum()
    p = x.sum() / N
    t = (s * (x - n * p)).sum()
    var = p * (1 - p) * ((n * s ** 2).sum() - (n * s).sum() ** 2 / N)
    z = t / math.sqrt(var)
    return z, 2 * stats.norm.sf(abs(z))


def gvif(exog, bloques):
    """VIF generalizado (Fox & Monette) por bloque de columnas. exog: DataFrame sin constante."""
    R = np.corrcoef(exog.values, rowvar=False)
    cols = list(exog.columns)
    det_all = np.linalg.det(R)
    out = {}
    for nombre, cs in bloques.items():
        i = [cols.index(c) for c in cs]
        j = [k for k in range(len(cols)) if k not in i]
        gv = np.linalg.det(R[np.ix_(i, i)]) * np.linalg.det(R[np.ix_(j, j)]) / det_all
        out[nombre] = (gv, gv ** (1 / (2 * len(i))), len(i))
    return out


def hosmer_lemeshow(y, p, g=10):
    """Prueba de Hosmer-Lemeshow con g grupos por deciles de probabilidad predicha."""
    d = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)})
    d["g"] = pd.qcut(d.p, g, duplicates="drop")
    t = d.groupby("g", observed=True).agg(n=("y", "size"), obs=("y", "sum"), esp=("p", "sum"))
    est = (((t.obs - t.esp) ** 2) / (t.esp * (1 - t.esp / t.n))).sum()
    gl = len(t) - 2
    return est, gl, stats.chi2.sf(est, gl)


def indices_bootstrap_cluster(grupos_idx, n_grupos, rng):
    """Remuestreo de conglomerados (hogares) con reposición. grupos_idx: lista de arrays de filas por hogar."""
    sel = rng.integers(0, n_grupos, n_grupos)
    return np.concatenate([grupos_idx[g] for g in sel])


def ic_percentil(v, nivel=0.95):
    a = (1 - nivel) / 2
    return float(np.quantile(v, a)), float(np.quantile(v, 1 - a))


def p_bootstrap_dos_colas(v, valor_nulo=0.0):
    """p bootstrap aproximado: 2 * min(P(v* <= nulo), P(v* >= nulo)), con suavizado +1."""
    v = np.asarray(v)
    b = len(v)
    pa = (np.sum(v <= valor_nulo) + 1) / (b + 1)
    pb = (np.sum(v >= valor_nulo) + 1) / (b + 1)
    return min(1.0, 2 * min(pa, pb))
