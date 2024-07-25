async function classifyImage() {
    const imageUpload = document.getElementById('imageUpload').files[0];
    if (!imageUpload) {
        alert("Please upload an image first.");
        return;
    }

    const formData = new FormData();
    formData.append('file', imageUpload);

    try {
        const response = await fetch('http://127.0.0.1:5000/classify_image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error: ' + response.statusText);
        }

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displayResult(result) {
    const resultDiv = document.getElementById('result');
    const classImageUrl = `http://127.0.0.1:5000/class_image/${result.classe}`;

    resultDiv.innerHTML = `
        <div class="result-container">
            <div class="class-details">
                <h2 class="class-name">Class: ${result.classe}</h2>
                <img src="${classImageUrl}" alt="Class Image" class="class-image">
            </div>
            <div class="nutritional-chart-container">
                <div class="nutritional-info">
                    <p class="calories">Calories: ${result.nutritional_info['calories par 100g(kcal)']}</p>
                    <p class="nutrient">Proteins: ${result.nutritional_info['proteins(%)']}%</p>
                    <p class="nutrient">Carbs: ${result.nutritional_info['carbs(%)']}%</p>
                    <p class="nutrient">Fats: ${result.nutritional_info['fats(%)']}%</p>
                </div>
                <canvas id="nutritionChart"></canvas>
            </div>
        </div>
    `;

    const ctx = document.getElementById('nutritionChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Proteins (%)', 'Carbs (%)', 'Fats (%)'],
            datasets: [{
                data: [
                    result.nutritional_info['proteins(%)'],
                    result.nutritional_info['carbs(%)'],
                    result.nutritional_info['fats(%)']
                ],
                backgroundColor: ['blue', 'orange', 'green'],
                borderColor: 'black',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        color: 'rgb(139, 217, 23)'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return `${tooltipItem.label}: ${tooltipItem.raw}%`;
                        }
                    },
                    bodyFont: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}
