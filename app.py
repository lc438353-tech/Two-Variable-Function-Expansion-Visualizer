import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Taylor Expansion Visualizer", page_icon="📈", layout="wide")

st.title("📈 Two-Variable Function Expansion Visualizer")
st.write("Explore second-order Taylor expansion, compare it with the original function, and visualize approximation error.")

FUNCTIONS = {
    "x² + xy + y²": {
        "f": lambda x, y: x**2 + x*y + y**2,
        "fx": lambda x, y: 2*x + y,
        "fy": lambda x, y: x + 2*y,
        "fxx": lambda x, y: 2 + 0*x + 0*y,
        "fxy": lambda x, y: 1 + 0*x + 0*y,
        "fyy": lambda x, y: 2 + 0*x + 0*y,
    },
    "x³ + y²": {
        "f": lambda x, y: x**3 + y**2,
        "fx": lambda x, y: 3*x**2,
        "fy": lambda x, y: 2*y,
        "fxx": lambda x, y: 6*x,
        "fxy": lambda x, y: 0*x + 0*y,
        "fyy": lambda x, y: 2 + 0*x + 0*y,
    },
    "sin(x) + cos(y)": {
        "f": lambda x, y: np.sin(x) + np.cos(y),
        "fx": lambda x, y: np.cos(x),
        "fy": lambda x, y: -np.sin(y),
        "fxx": lambda x, y: -np.sin(x),
        "fxy": lambda x, y: 0*x + 0*y,
        "fyy": lambda x, y: -np.cos(y),
    },
    "exp(x) × cos(y)": {
        "f": lambda x, y: np.exp(x) * np.cos(y),
        "fx": lambda x, y: np.exp(x) * np.cos(y),
        "fy": lambda x, y: -np.exp(x) * np.sin(y),
        "fxx": lambda x, y: np.exp(x) * np.cos(y),
        "fxy": lambda x, y: -np.exp(x) * np.sin(y),
        "fyy": lambda x, y: -np.exp(x) * np.cos(y),
    },
}

with st.sidebar:
    st.header("⚙️ Settings")
    function_name = st.selectbox("Choose a function", list(FUNCTIONS.keys()))
    st.caption("For sin, cos, and exp, angles are in radians.")
    a = st.number_input("Expansion point a (x-coordinate)", value=1.0, step=0.1)
    b = st.number_input("Expansion point b (y-coordinate)", value=1.0, step=0.1)
    h = st.number_input("Increment h", value=0.1, step=0.1, format="%.3f")
    k = st.number_input("Increment k", value=-0.1, step=0.1, format="%.3f")
    span = st.slider("Graph range around expansion point", 0.5, 5.0, 2.0, 0.5)

d = FUNCTIONS[function_name]
x, y = a + h, b + k

f0 = float(d["f"](a, b))
fx = float(d["fx"](a, b))
fy = float(d["fy"](a, b))
fxx = float(d["fxx"](a, b))
fxy = float(d["fxy"](a, b))
fyy = float(d["fyy"](a, b))

approx = f0 + h*fx + k*fy + 0.5*(h*h*fxx + 2*h*k*fxy + k*k*fyy)
actual = float(d["f"](x, y))
error = abs(actual - approx)
relative_error = (error / abs(actual) * 100) if abs(actual) > 1e-12 else None

st.subheader("Results")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Expansion point", f"({a:.3f}, {b:.3f})")
c2.metric("Target point", f"({x:.3f}, {y:.3f})")
c3.metric("Taylor approximation", f"{approx:.6f}")
c4.metric("Actual value", f"{actual:.6f}")

st.metric("Absolute error", f"{error:.8f}", help="Absolute difference between the actual function value and the Taylor approximation.")
if relative_error is not None:
    st.caption(f"Relative error: {relative_error:.6f}%")

st.latex(r"f(a+h,b+k)\approx f(a,b)+hf_x+kf_y+\\frac{1}{2}\\left(h^2f_{xx}+2hkf_{xy}+k^2f_{yy}\\right)")
st.write(f"**Selected function:** `{function_name}`")

with st.expander("See derivative values at the expansion point"):
    st.latex(rf"f(a,b)={f0:.6f}")
    st.latex(rf"f_x(a,b)={fx:.6f},\\quad f_y(a,b)={fy:.6f}")
    st.latex(rf"f_{{xx}}(a,b)={fxx:.6f},\\quad f_{{xy}}(a,b)={fxy:.6f},\\quad f_{{yy}}(a,b)={fyy:.6f}")
    st.write("These values are substituted into the second-order Taylor formula.")

st.subheader("3D surface: original function")
xs = np.linspace(a-span, a+span, 45)
ys = np.linspace(b-span, b+span, 45)
X, Y = np.meshgrid(xs, ys)
Z = d["f"](X, Y)
fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", opacity=0.88)])
fig.add_trace(go.Scatter3d(x=[a], y=[b], z=[f0], mode="markers+text",
                           marker=dict(size=6, color="red"),
                           text=["Expansion point"], textposition="top center",
                           name="Expansion point"))
fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[actual], mode="markers+text",
                           marker=dict(size=6, color="orange"),
                           text=["Target point"], textposition="top center",
                           name="Target point"))
fig.update_layout(scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="f(x,y)"),
                  margin=dict(l=0, r=0, t=20, b=0), height=550)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Approximation error as the target point moves")
steps = np.linspace(-0.5, 0.5, 41)
errors = []
for dh in steps:
    for dk in steps:
        pred = f0 + dh*fx + dk*fy + 0.5*(dh*dh*fxx + 2*dh*dk*fxy + dk*dk*fyy)
        truth = float(d["f"](a+dh, b+dk))
        errors.append((dh, dk, abs(truth-pred)))
E = np.array(errors)
err_fig = go.Figure(data=go.Scatter3d(x=E[:, 0], y=E[:, 1], z=E[:, 2],
                                     mode="markers", marker=dict(size=3, color=E[:, 2], colorscale="Plasma",
                                                                  colorbar=dict(title="Absolute error"))))
err_fig.update_layout(scene=dict(xaxis_title="h", yaxis_title="k", zaxis_title="Absolute error"),
                      margin=dict(l=0, r=0, t=20, b=0), height=450)
st.plotly_chart(err_fig, use_container_width=True)

st.info("Tip: Taylor approximation is usually most accurate near the expansion point. For a quadratic function, the second-order expansion is exact (up to floating-point rounding).")
st.caption("Educational project • Python • Streamlit • NumPy • Plotly")
