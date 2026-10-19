# Two-Variable Function Expansion Visualizer

An interactive B.Tech Engineering Mathematics project that demonstrates second-order Taylor expansion for functions of two variables.

## Features
- Choose among four example functions
- Set expansion point `(a, b)` and increments `(h, k)`
- Compare Taylor approximation with the actual function value
- Calculate absolute and relative error
- Inspect first- and second-order partial derivatives
- Explore an interactive 3D function surface and a 3D error plot

## Run on Windows

1. Install Python 3.10 or newer.
2. Open PowerShell in this project folder.
3. (Recommended) Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Formula

For a function `f(x, y)`, the second-order Taylor approximation around `(a, b)` is:

`f(a+h,b+k) ≈ f(a,b) + h f_x + k f_y + 1/2 (h² f_xx + 2hk f_xy + k² f_yy)`

All derivatives are evaluated at `(a, b)`.

## Project algorithm
1. Select a function and expansion point.
2. Calculate the first- and second-order partial derivatives at that point.
3. Substitute the derivatives and increments into the second-order Taylor formula.
4. Evaluate the original function at the target point `(a+h, b+k)`.
5. Calculate absolute error.
6. Display numerical results and interactive graphs.

## Note
This is an educational visualizer. The derivatives for the listed functions are coded explicitly; it does not accept arbitrary typed formulas.
