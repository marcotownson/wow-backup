import subprocess
import markdown
import base64
import os

def run_and_render():
    """Runs the consolidated_analyzer.py script, captures its output,
    converts it to HTML with styling, embeds the images and LLM response, 
    and saves it to a file."""

    # Run the script and capture the output
    result = subprocess.run(['python3', 'archive/phase2/consolidated_analyzer.py'], capture_output=True, text=True)
    output = result.stdout

    # Encode the images in base64
    image_filenames = [
        "image_20x15_Orientation.png",
        "image_15x20_Orientation.png",
        "timeseries_plot.png",
        "fft_plot.png",
        "ngram_frequencies.png",
        os.path.join("wow_signal_final_candidate", "final_bitmap.png"),
        os.path.join("wow_signal_final_candidate", "final_sphere_map.png"),
        os.path.join("wow_signal_final_candidate", "final_quantum_evolution.png"),
        "even_row_parity_layer.png",
        "odd_row_parity_layer.png",
        "even_col_parity_layer.png",
        "odd_col_parity_layer.png",
        "composite_image.png",
        os.path.join("wow_signal_final_candidate", "analysis_force_vectors.png"),
        os.path.join("wow_signal_final_candidate", "analysis_kinetic_energy.png")
    ]
    
    encoded_images = {}
    for filename in image_filenames:
        try:
            with open(filename, "rb") as image_file:
                encoded_images[filename] = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            encoded_images[filename] = None
            
    # Read the Llama response
    try:
        with open("llama_response.md", "r") as f:
            llama_response = f.read()
        llama_html = markdown.markdown(llama_response)
    except FileNotFoundError:
        llama_html = "<p>Llama response not found.</p>"

    # Create the full HTML content with styling
    html_content = f"""
    <html>
    <head>
        <title>WoW! Signal Analysis</title>
        <style>
            body {{
                font-family: sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #005a9c;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
            }}
            .llama-response {{
                background-color: #eef8ff;
                border-left: 5px solid #005a9c;
                padding: 15px;
                margin-top: 20px;
            }}
            .collapsible {{
                background-color: #777;
                color: white;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 15px;
            }}
            .active, .collapsible:hover {{
                background-color: #555;
            }}
            .content {{
                padding: 0 18px;
                display: none;
                overflow: hidden;
                background-color: #f1f1f1;
            }}
        </style>
    </head>
    <body>
        <h1>WoW! Signal Analysis Report</h1>
        <h2>Llama Analysis</h2>
        <div class="llama-response">
            {llama_html}
        </div>
        
        <button type="button" class="collapsible">Show Raw Output</button>
        <div class="content">
            <pre>{output}</pre>
        </div>

        <h2>Visualizations</h2>
        {'<img src="data:image/png;base64,{}" alt="20x15 Orientation">'.format(encoded_images["image_20x15_Orientation.png"]) if encoded_images["image_20x15_Orientation.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="15x20 Orientation">'.format(encoded_images["image_15x20_Orientation.png"]) if encoded_images["image_15x20_Orientation.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Timeseries Plot">'.format(encoded_images["timeseries_plot.png"]) if encoded_images["timeseries_plot.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="FFT Plot">'.format(encoded_images["fft_plot.png"]) if encoded_images["fft_plot.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="N-gram Frequencies">'.format(encoded_images["ngram_frequencies.png"]) if encoded_images["ngram_frequencies.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Final Bitmap">'.format(encoded_images[os.path.join("wow_signal_final_candidate", "final_bitmap.png")]) if encoded_images[os.path.join("wow_signal_final_candidate", "final_bitmap.png")] else ''}
        {'<img src="data:image/png;base64,{}" alt="Final Sphere Map">'.format(encoded_images[os.path.join("wow_signal_final_candidate", "final_sphere_map.png")]) if encoded_images[os.path.join("wow_signal_final_candidate", "final_sphere_map.png")] else ''}
        {'<img src="data:image/png;base64,{}" alt="Final Quantum Evolution">'.format(encoded_images[os.path.join("wow_signal_final_candidate", "final_quantum_evolution.png")]) if encoded_images[os.path.join("wow_signal_final_candidate", "final_quantum_evolution.png")] else ''}
        {'<img src="data:image/png;base64,{}" alt="Even Row Parity Layer">'.format(encoded_images["even_row_parity_layer.png"]) if encoded_images["even_row_parity_layer.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Odd Row Parity Layer">'.format(encoded_images["odd_row_parity_layer.png"]) if encoded_images["odd_row_parity_layer.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Even Column Parity Layer">'.format(encoded_images["even_col_parity_layer.png"]) if encoded_images["even_col_parity_layer.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Odd Column Parity Layer">'.format(encoded_images["odd_col_parity_layer.png"]) if encoded_images["odd_col_parity_layer.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Composite Image">'.format(encoded_images["composite_image.png"]) if encoded_images["composite_image.png"] else ''}
        {'<img src="data:image/png;base64,{}" alt="Force Vectors">'.format(encoded_images[os.path.join("wow_signal_final_candidate", "analysis_force_vectors.png")]) if encoded_images[os.path.join("wow_signal_final_candidate", "analysis_force_vectors.png")] else ''}
        {'<img src="data:image/png;base64,{}" alt="Kinetic Energy">'.format(encoded_images[os.path.join("wow_signal_final_candidate", "analysis_kinetic_energy.png")]) if encoded_images[os.path.join("wow_signal_final_candidate", "analysis_kinetic_energy.png")] else ''}
        
        <script>
            var coll = document.getElementsByClassName("collapsible");
            var i;

            for (i = 0; i < coll.length; i++) {{
                coll[i].addEventListener("click", function() {{
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {{
                        content.style.display = "none";
                    }} else {{
                        content.style.display = "block";
                    }}
                }});
            }}
        </script>
    </body>
    </html>
    """

    # Write the HTML to a file
    with open('output.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    run_and_render()
