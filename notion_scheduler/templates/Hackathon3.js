document.getElementById('generateTasks').addEventListener('click', generateTasks);

function generateTasks() {
  // Example tasks (replace with real AI-generated tasks)
  const tasks = [
    { id: 1, task: 'Book venue', status: 'pending' },
    { id: 2, task: 'Send invites', status: 'pending' },
    { id: 3, task: 'Order catering', status: 'pending' },
  ];

  // Clear previous tasks
  const taskTableBody = document.querySelector('#taskTable tbody');
  taskTableBody.innerHTML = '';

  // Add tasks to the table
  tasks.forEach((task) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${task.id}</td>
      <td>${task.task}</td>
      <td class="status">${task.status}</td>
      <td>
        <button class="keep-btn">Keep</button>
        <button class="discard-btn">Discard</button>
      </td>
    `;
    taskTableBody.appendChild(row);

    // Attach event listeners to "Keep" and "Discard" buttons
    row.querySelector('.keep-btn').addEventListener('click', () => updateStatus(task.id, 'kept'));
    row.querySelector('.discard-btn').addEventListener('click', () => updateStatus(task.id, 'discarded'));
  });
}

function updateStatus(taskId, newStatus) {
  const taskRows = document.querySelectorAll('#taskTable tbody tr');
  taskRows.forEach((row) => {
    const taskCell = row.cells[0].textContent;
    if (parseInt(taskCell) === taskId) {
      const statusCell = row.querySelector('.status');
      statusCell.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
      statusCell.style.color = newStatus === 'kept' ? 'green' : 'red';
    }
  });
}
