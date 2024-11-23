// Handle Task Generation
document.getElementById('generateTasks').addEventListener('click', () => {
    // Get form values
    const eventName = document.getElementById('eventName').value;
    const eventDuration = document.getElementById('eventDuration').value;
  
    if (!eventName || !eventDuration) {
      alert("Please fill in all fields.");
      return;
    }
  
    // Placeholder tasks (replace with AI-generated tasks later)
    const placeholderTasks = [
      "Set up venue",
      "Send invitations",
      "Prepare food and drinks",
      "Arrange decorations",
      "Create a schedule"
    ];
  
    // Clear existing table rows
    const taskTableBody = document.getElementById('taskTable').querySelector('tbody');
    taskTableBody.innerHTML = "";
  
    // Populate table with tasks
    placeholderTasks.forEach((task, index) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${task}</td>
        <td>
          <input type="checkbox">
        </td>
      `;
      taskTableBody.appendChild(row);
    });
  
    alert(`Tasks generated for ${eventName} (Duration: ${eventDuration} hours)!`);
  });
  