import numpy as np
import pandas as pd
import shap


def get_vips(x, model):
    t = model.x_scores_
    w = model.x_weights_
    q = model.y_loadings_

    m, p = x.shape
    _, h = t.shape

    vips = np.zeros((p,))

    s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
    total_s = np.sum(s)

    for i in range(p):
        weight = np.array([(w[i, j] / np.linalg.norm(w[:, j])) ** 2 for j in range(h)])
        vips[i] = np.sqrt(p * (s.T @ weight) / total_s)

    return vips


def get_shap(x, model):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(x)
    shap_mean = pd.DataFrame(shap_values, columns=x.columns).apply(lambda x: abs(x)).mean()
    # shap.summary_plot(shap_values, x, plot_type="bar")
    return shap_mean.sort_values(ascending=False)
