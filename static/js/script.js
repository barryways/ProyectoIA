document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('inputForm');
    const responseDiv = document.getElementById('response');
    const responseTimeDiv = document.getElementById('responseTime');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent form from refreshing the page

        const userInput = document.getElementById('userInput').value;
        const startTime = performance.now();

        try {
            const response = await fetch('/api/v1/analyst', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input: userInput }),
            });

            const data = await response.json();
            const endTime = performance.now();

            responseDiv.textContent = `La noticia es de: ${data.data}`;
            responseTimeDiv.textContent = `El tiempo de respuesta fué de: ${(endTime - startTime).toFixed(2)} ms`;
        } catch (error) {
            responseDiv.textContent = 'Error: Unable to fetch response.';
        }
    });
});