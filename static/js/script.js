document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('inputForm');
    const responseDiv = document.getElementById('response');
    const responseTimeDiv = document.getElementById('responseTime');
    const metricsDiv = document.getElementById('metrics');
    const tbody = document.querySelector('#metricsTable tbody');
  
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      // Limpieza antes de cada envío
      responseDiv.textContent = '';
      responseTimeDiv.textContent = '';
      metricsDiv.style.display = 'none';
      tbody.innerHTML = '';
  
      const userInput = document.getElementById('userInput').value;
      const startTime = performance.now();
  
      try {
        const res = await fetch('/api/v1/analyst', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input: userInput }),
        });
  
        // Comprueba que no haya error HTTP
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
  
        const data = await res.json();
        const endTime = performance.now();
        const duration = (endTime - startTime).toFixed(2);
  
        // Mostrar categoría
        responseDiv.textContent = `La noticia es de: ${data.categoria}`;
  
        // Pintar métricas
        for (let cat in data.precision) {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${cat}</td>
            <td>${data.precision[cat].toFixed(2)}</td>
            <td>${data.recall[cat].toFixed(2)}</td>
            <td>${data.f1_score[cat].toFixed(2)}</td>
          `;
          tbody.appendChild(tr);
        }
        metricsDiv.style.display = 'block';
  
        // Tiempo de respuesta
        responseTimeDiv.textContent = `Tiempo de respuesta: ${duration} ms`;
  
      } catch (error) {
        console.error('Fetch error:', error);
        responseDiv.textContent = `Error: ${error.message}`;
      }
    });
  });
  