// Configuración de la API - Usamos URL relativa
const API_URL = '';

// Elementos del DOM
const incidentsContainer = document.getElementById('incidents-container');
const loadingMessage = document.getElementById('loading');
const incidentForm = document.getElementById('incident-form');
const reporterInput = document.getElementById('reporter');
const descriptionInput = document.getElementById('description');

// Evento de envío del formulario para crear incidentes
incidentForm.addEventListener('submit', createIncident);

// Cargar incidentes al cargar la página
document.addEventListener('DOMContentLoaded', loadIncidents);

// Función para cargar todos los incidentes
async function loadIncidents() {
    try {
        loadingMessage.style.display = 'block';
        
        const response = await fetch(`${API_URL}/incidents`);
        
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        
        const incidents = await response.json();
        
        // Limpiar contenedor
        incidentsContainer.innerHTML = '';
        
        if (incidents.length === 0) {
            incidentsContainer.innerHTML = '<p>No hay incidentes registrados.</p>';
            return;
        }
        
        // Mostrar cada incidente
        incidents.forEach(incident => {
            displayIncident(incident);
        });
        
    } catch (error) {
        console.error('Error al cargar los incidentes:', error);
        incidentsContainer.innerHTML = '<p>Error al cargar los incidentes. Intenta de nuevo.</p>';
    } finally {
        loadingMessage.style.display = 'none';
    }
}

// Función para mostrar un incidente en el DOM
function displayIncident(incident) {
    const incidentElement = document.createElement('div');
    incidentElement.className = 'incident';
    incidentElement.dataset.id = incident.id;
    
    // Formatear fecha
    const date = new Date(incident.created_at);
    const formattedDate = date.toLocaleString();
    
    // HTML del incidente
    incidentElement.innerHTML = `
        <h3>Incidente #${incident.id}</h3>
        <p><strong>Reportado por:</strong> ${incident.reporter}</p>
        <p><strong>Descripción:</strong> ${incident.description}</p>
        <p><strong>Estado:</strong> <span class="status-${incident.status.replace(' ', '-')}">${incident.status}</span></p>
        <p><strong>Fecha:</strong> ${formattedDate}</p>
        
        <div class="action-buttons">
            <select class="status-select">
                <option value="pendiente" ${incident.status === 'pendiente' ? 'selected' : ''}>Pendiente</option>
                <option value="en proceso" ${incident.status === 'en proceso' ? 'selected' : ''}>En Proceso</option>
                <option value="resuelto" ${incident.status === 'resuelto' ? 'selected' : ''}>Resuelto</option>
            </select>
            <button class="update-btn">Actualizar Estado</button>
            <button class="delete">Eliminar</button>
        </div>
    `;
    
    // Agregar eventos a los botones
    const updateBtn = incidentElement.querySelector('.update-btn');
    const deleteBtn = incidentElement.querySelector('.delete');
    const statusSelect = incidentElement.querySelector('.status-select');
    
    updateBtn.addEventListener('click', () => updateIncidentStatus(incident.id, statusSelect.value));
    deleteBtn.addEventListener('click', () => deleteIncident(incident.id));
    
    incidentsContainer.appendChild(incidentElement);
}

// Función para crear un nuevo incidente
async function createIncident(event) {
    event.preventDefault();
    
    const reporter = reporterInput.value.trim();
    const description = descriptionInput.value.trim();
    
    if (!reporter || !description) {
        alert('Por favor completa todos los campos');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/incidents`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reporter: reporter,
                description: description
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al crear el incidente');
        }
        
        const newIncident = await response.json();
        
        // Limpiar formulario
        incidentForm.reset();
        
        // Mostrar el nuevo incidente
        displayIncident(newIncident);
        
        alert('Incidente creado con éxito');
        
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

// Función para actualizar el estado de un incidente
async function updateIncidentStatus(id, newStatus) {
    try {
        const response = await fetch(`${API_URL}/incidents/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: newStatus
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al actualizar el incidente');
        }
        
        const updatedIncident = await response.json();
        
        // Actualizar la UI
        const incidentElement = document.querySelector(`.incident[data-id="${id}"]`);
        const statusSpan = incidentElement.querySelector('span[class^="status-"]');
        
        // Actualizar clase y texto
        statusSpan.className = `status-${newStatus.replace(' ', '-')}`;
        statusSpan.textContent = newStatus;
        
        alert('Estado actualizado con éxito');
        
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

// Función para eliminar un incidente
async function deleteIncident(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este incidente?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/incidents/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Incidente no encontrado');
            }
            throw new Error('Error al eliminar el incidente');
        }
        
        // Eliminar de la UI
        const incidentElement = document.querySelector(`.incident[data-id="${id}"]`);
        incidentElement.remove();
        
        alert('Incidente eliminado con éxito');
        
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}