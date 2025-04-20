const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const dueDateInput = document.getElementById('due-date');
const taskList = document.getElementById('task-list');

taskForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const taskText = taskInput.value.trim();
  const dueDate = dueDateInput.value;

  if (taskText !== '') {
    addTask(taskText, dueDate);
    taskInput.value = '';
    dueDateInput.value = '';
  }
});

function addTask(text, dueDate) {
  const li = document.createElement('li');
  li.innerHTML = `
    <span>${text} ${dueDate ? `(Prazo: ${dueDate})` : ''}</span>
    <div class="task-buttons">
      <button onclick="completeTask(this)">Concluir</button>
      <button onclick="deleteTask(this)">Excluir</button>
    </div>
  `;
  taskList.appendChild(li);
}

function completeTask(button) {
  const li = button.parentElement.parentElement;
  li.classList.toggle('completed');
}

function deleteTask(button) {
  const li = button.parentElement.parentElement;
  taskList.removeChild(li);
}
