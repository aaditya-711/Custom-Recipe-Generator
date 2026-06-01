from boltiotai import openai
import os
from flask import Flask, render_template_string, request

# Set OpenAI API Key
openai.api_key = "BOLT_API_KEY_HERE"

# Initialize Flask App
app = Flask(__name__)


# Function to Generate Recipe
def generate_tutorial(components):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant"
                },
                {
                    "role": "user",
                    "content": f"""
Suggest a recipe using the items listed as available.

Requirements:
- Give the recipe a nice name
- Add a funny version of the recipe name
- Explain the recipe step-by-step
- End with a fun fact

Available ingredients:
{components},
Haldi,
Chilly Powder,
Tomato Ketchup,
Water,
Garam Masala,
Oil
"""
                }
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error gathering recipe: {str(e)}"


# Main Route (Only handles loading the initial page structure)
@app.route('/', methods=['GET'])
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --cream: #fdf6ec;
            --warm: #f5e6cc;
            --orange: #e8631a;
            --orange-light: #f28444;
            --brown: #3d1f0a;
            --brown-mid: #7a3b10;
            --green: #4a6741;
            --text: #2c1a0e;
            --muted: #8a6a52;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'DM Sans', sans-serif;
            background-color: var(--cream);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: -120px; right: -120px;
            width: 500px; height: 500px;
            background: radial-gradient(circle, #f5c98855 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }
        body::after {
            content: '';
            position: fixed;
            bottom: -100px; left: -100px;
            width: 400px; height: 400px;
            background: radial-gradient(circle, #c8e6c044 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }

        .page-wrap {
            position: relative;
            z-index: 1;
            max-width: 780px;
            margin: 0 auto;
            padding: 60px 24px 80px;
        }

        header {
            text-align: center;
            margin-bottom: 52px;
            animation: fadeDown 0.7s ease both;
        }

        .badge {
            display: inline-block;
            background: var(--green);
            color: #fff;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
        }

        h1 {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.4rem, 6vw, 3.6rem);
            color: var(--brown);
            line-height: 1.15;
            margin-bottom: 14px;
        }

        h1 span { color: var(--orange); font-style: italic; }

        .subtitle {
            color: var(--muted);
            font-size: 1rem;
            font-weight: 300;
            max-width: 420px;
            margin: 0 auto;
            line-height: 1.6;
        }

        .divider {
            display: flex;
            align-items: center;
            gap: 14px;
            margin: 0 auto 44px;
            max-width: 340px;
        }
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(to right, transparent, #c9a87888);
        }
        .divider::after { background: linear-gradient(to left, transparent, #c9a87888); }

        .card {
            background: #fff;
            border-radius: 24px;
            box-shadow: 0 8px 40px rgba(61,31,10,0.09), 0 2px 8px rgba(61,31,10,0.05);
            overflow: hidden;
            animation: fadeUp 0.7s ease 0.15s both;
        }

        .card-top {
            background: linear-gradient(135deg, var(--brown) 0%, var(--brown-mid) 100%);
            padding: 32px 36px 28px;
            position: relative;
            overflow: hidden;
        }
        .card-top::after {
            content: '🍳';
            position: absolute;
            right: 28px; top: 50%;
            transform: translateY(-50%);
            font-size: 4rem;
            opacity: 0.18;
        }

        .card-top label {
            display: block;
            color: #f5c988;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .input-row { display: flex; gap: 12px; align-items: center; }

        .input-row input {
            flex: 1;
            background: rgba(255,255,255,0.12);
            border: 1.5px solid rgba(255,255,255,0.22);
            border-radius: 12px;
            padding: 14px 18px;
            color: #fff;
            font-size: 1rem;
            font-family: 'DM Sans', sans-serif;
            outline: none;
            transition: border 0.2s, background 0.2s;
        }
        .input-row input::placeholder { color: rgba(255,255,255,0.45); }
        .input-row input:focus {
            border-color: var(--orange-light);
            background: rgba(255,255,255,0.18);
        }

        .btn-generate {
            background: linear-gradient(135deg, var(--orange) 0%, var(--orange-light) 100%);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 14px 26px;
            font-size: 0.95rem;
            font-weight: 500;
            font-family: 'DM Sans', sans-serif;
            cursor: pointer;
            white-space: nowrap;
            transition: transform 0.15s, box-shadow 0.15s;
            box-shadow: 0 4px 16px rgba(232,99,26,0.35);
        }
        .btn-generate:hover { transform: translateY(-2px); box-shadow: 0 6px 22px rgba(232,99,26,0.45); }
        .btn-generate:active { transform: translateY(0); }
        .btn-generate:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }

        .chips {
            padding: 18px 36px;
            background: var(--warm);
            border-bottom: 1px solid #e8d5bb;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        .chips-label {
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--muted);
            margin-right: 4px;
        }
        .chip {
            background: #fff;
            border: 1px solid #ddc9a8;
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 12px;
            color: var(--brown-mid);
        }

        .output-section { padding: 32px 36px 36px; }

        .output-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .output-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem;
            color: var(--brown);
        }

        .btn-copy {
            background: transparent;
            border: 1.5px solid #ddc9a8;
            border-radius: 8px;
            padding: 7px 16px;
            font-size: 12px;
            font-family: 'DM Sans', sans-serif;
            color: var(--muted);
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-copy:hover { border-color: var(--orange); color: var(--orange); background: #fff5ee; }

        .output-box {
            background: var(--cream);
            border: 1.5px solid #e8d5bb;
            border-radius: 16px;
            padding: 28px;
            min-height: 160px;
        }

        .output-box pre {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95rem;
            line-height: 1.85;
            color: var(--text);
            white-space: pre-wrap;
            word-break: break-word;
        }

        .placeholder-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 32px 0;
            color: var(--muted);
        }
        .placeholder-state .icon { font-size: 2.8rem; opacity: 0.5; }
        .placeholder-state p { font-size: 0.92rem; font-weight: 300; }

        .spinner {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 16px;
            padding: 32px 0;
        }
        .spinner.active { display: flex; }
        .spinner-ring {
            width: 44px; height: 44px;
            border: 3px solid #e8d5bb;
            border-top-color: var(--orange);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        .spinner p { font-size: 0.9rem; color: var(--muted); font-weight: 300; }

        @keyframes fadeDown {
            from { opacity: 0; transform: translateY(-18px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(22px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .result-appear { animation: fadeIn 0.5s ease both; }

        footer {
            text-align: center;
            margin-top: 40px;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 300;
            animation: fadeUp 0.7s ease 0.3s both;
        }

        @media (max-width: 560px) {
            .page-wrap { padding: 36px 16px 60px; }
            .card-top, .chips, .output-section { padding-left: 20px; padding-right: 20px; }
            .input-row { flex-direction: column; }
            .btn-generate { width: 100%; }
        }
    </style>
</head>
<body>

<div class="page-wrap">

    <header>
        <div class="badge">✦ AI-Powered</div>
        <h1>Custom <span>Recipe</span><br>Generator</h1>
        <p class="subtitle">Enter what's in your kitchen and get a delicious recipe instantly.</p>
    </header>

    <div class="divider"><span>🌿</span></div>

    <div class="card">

        <div class="card-top">
            <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();">
                <label for="components">What ingredients do you have?</label>
                <div class="input-row">
                    <input
                        type="text"
                        id="components"
                        name="components"
                        placeholder="e.g. Bread, Potato, Paneer, Eggs..."
                        required
                        autocomplete="off"
                    >
                    <button type="submit" class="btn-generate" id="gen-btn">✦ Generate</button>
                </div>
            </form>
        </div>

        <div class="chips">
            <span class="chips-label">Always included</span>
            <span class="chip">🟡 Haldi</span>
            <span class="chip">🌶 Chilly Powder</span>
            <span class="chip">🍅 Tomato Ketchup</span>
            <span class="chip">💧 Water</span>
            <span class="chip">🫙 Garam Masala</span>
            <span class="chip">🫒 Oil</span>
        </div>

        <div class="output-section">
            <div class="output-header">
                <div class="output-title">🍽 Your Recipe</div>
                <button class="btn-copy" onclick="copyToClipboard()">📋 Copy</button>
            </div>

            <div class="output-box">
                <div class="spinner" id="spinner">
                    <div class="spinner-ring"></div>
                    <p>Cooking up your recipe...</p>
                </div>

                <pre id="output"></pre>

                <div class="placeholder-state" id="placeholder">
                    <div class="icon">👨‍🍳</div>
                    <p>Your recipe will appear here</p>
                </div>
            </div>
        </div>

    </div>

    <footer>Made with ❤️ &amp; a pinch of AI spice</footer>

</div>

<script>
    async function generateTutorial() {
        const output = document.querySelector('#output');
        const spinner = document.querySelector('#spinner');
        const placeholder = document.querySelector('#placeholder');
        const btn = document.querySelector('#gen-btn');

        if (placeholder) placeholder.style.display = 'none';
        output.textContent = '';
        spinner.classList.add('active');
        btn.disabled = true;
        btn.textContent = '⏳ Cooking...';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: new FormData(document.querySelector('#tutorial-form'))
            });
            const result = await response.text();

            spinner.classList.remove('active');
            output.textContent = result;
            output.classList.add('result-appear');
        } catch (error) {
            spinner.classList.remove('active');
            output.textContent = "Oops! Something went wrong while requesting the recipe.";
            if (placeholder) placeholder.style.display = 'flex';
        }

        btn.disabled = false;
        btn.textContent = '✦ Generate';
    }

    function copyToClipboard() {
        const output = document.querySelector('#output');
        if (!output.textContent.trim()) return;
        navigator.clipboard.writeText(output.textContent);
        const btn = document.querySelector('.btn-copy');
        btn.innerHTML = '✅ Copied!';
        setTimeout(() => btn.innerHTML = '📋 Copy', 2000);
    }
</script>

</body>
</html>
""")


# Generate Route (Explicitly handles the asynchronous processing request)
@app.route('/generate', methods=['POST'])
def generate():
    components = request.form.get('components', '')
    return generate_tutorial(components)


# Run Flask App
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )