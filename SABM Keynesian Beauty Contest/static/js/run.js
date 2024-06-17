document.getElementById('run-button').onclick = function() {
    fetch('/run-simulations', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        // 更新结果显示
        document.getElementById('results').innerHTML = `<b>Results:</b> <span class="results-text">${data.results.join(', ')}</span>`;
                
        // 更新图像显示
        document.getElementById('plot').src = `/get-plot?path=${data.plot_path}&timestamp=${new Date().getTime()}`;
    })
    .catch(error => console.error('Error:', error));
};
