<script setup>
import { ref, computed, watch } from 'vue'
import { Icon } from '@iconify/vue'

const filters = {
  all: function (todos) {
    return todos;
  },
  complete: function (todos) {
    return todos.filter(function (todo) {
      return todo.complete;
    });
  },
  incomplete: function (todos) {
    return todos.filter(function (todo) {
      return !todo.complete;
    });
  }
}

const STORAGE_KEY = 'vue-js-todo-P7oZi9sL'
const todoStorage = {
  fetch: function () {
    var todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    return todos;
  },
  save: function (todos) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
  }
}

const inputVal = ref('')
const todos = ref(todoStorage.fetch())
const visibility = ref('all')

watch(todos, function (todos) {
  todoStorage.save(todos);
}, { deep: true })

const filteredTodos = computed(function () {
  return filters[visibility.value](todos.value);
})

function addTodo(e) {
  e.preventDefault();
  if (inputVal.value) {
    todos.value.push({
      text: inputVal.value,
      complete: false
    });
  }
  inputVal.value = '';
}

function toggleTodo(todo) {
  todo.complete = !todo.complete;
}

function filterTodos(filter) {
  visibility.value = filter;
}

function deleteTodo(index) {
  todos.value.splice(index, 1);
}
</script>


<template>
<div class="app" id="app">
  <form class="form" v-on:submit="addTodo">
    <input class="input form__input" v-model="inputVal"/>
    <button class="btn form__submit-btn" type="submit">Add</button>
  </form>
  <transition-group tag="ol" name="list" class="todo-list">
    <li
      class="todo-list__item"
      v-bind:class="{ complete: todo.complete }"
      v-bind:key="index"
      v-for="(todo, index) in filteredTodos">
      <button
        class="todo-list__item-content"
        v-on:click="toggleTodo(todo)">
        {{ todo.text }}
      </button>
      <button
        class="btn todo-list__item-remove"
        v-on:click="deleteTodo(index)">
        <Icon :icon="todo.complete ? 'fa7-solid:check' : 'fa7-solid:times'"/>
      </button>
    </li>
  </transition-group>
  <div class="filters">
    <button 
      class="btn filters__btn filters__btn--all" 
      v-on:click="filterTodos('all')">
      All
    </button>
    <button 
      class="btn filters__btn filters__btn--complete" 
      v-on:click="filterTodos('complete')">
      Complete
    </button>
    <button 
      class="btn filters__btn filters__btn--incomplete" 
      v-on:click="filterTodos('incomplete')">
      Incomplete
    </button>
  </div>
</div>
</template>


<style scoped>
*, *:before, *:after {
  box-sizing: border-box;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-feature-settings: "liga", "kern";
  overflow-y: scroll;
  overflow-x: hidden;
  height: 100%;
  background: linear-gradient(210deg, #9adbbe, #4fc08d);
}

body {
  overflow: hidden;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Source Sans Pro", sans-serif;
}

button {
  background: none;
  border: none;
  color: inherit;
  font-size: inherit;
  font-family: inherit;
  font-weight: inherit;
}
button:focus {
  outline: none;
}
button:hover {
  cursor: pointer;
}

.app {
  min-height: 50vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  border-radius: 1em;
  background: #fff;
  overflow: hidden;
  box-shadow: 0 0 5px rgba(25, 25, 25, 0.25);
}

.btn {
  font-size: 14px;
  margin: 0 0.5em;
  border-radius: 2em;
  padding: 0.75em 1.5em;
  cursor: pointer;
  background: none;
  color: #2d7c58;
  border: 1px solid;
  letter-spacing: 1px;
  font-family: "Source Sans Pro", sans-serif;
  color: #4fc08d;
  border: #4fc08d 1px solid;
  transition: 250ms ease-out;
}
.btn:hover, .btn:focus {
  color: #fff;
  background: #4fc08d;
}

.form {
  width: 100%;
  padding: 1.5rem 1rem 0 1rem;
  display: flex;
}
.form__input {
  width: 100%;
  font-size: 14px;
  margin: 0 0.5em;
  border-radius: 2em;
  padding: 0.75em 1.5em;
  background: none;
  font-family: "Source Sans Pro", sans-serif;
  border: #e3e3e3 1px solid;
  transition: border 250ms ease-out;
}
.form__input:focus {
  border: #4fc08d 1px solid;
  outline: none;
}
.todo-list {
  width: 100%;
  padding: 0 1rem;
  flex: 1;
}
.todo-list__item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5em;
  margin-bottom: 0.5em;
  border-radius: 3px;
  transition: 200ms;
  color: #4fc08d;
}
.todo-list__item:last-child {
  margin-bottom: 0;
}
.todo-list__item.complete {
  color: lightgreen;
}
.todo-list__item.complete .todo-list__item-content:after {
  background: lightgreen;
}
.todo-list__item-content {
  position: relative;
}
.todo-list__item-content:after {
  content: "";
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  height: 1px;
  background: #4fc08d;
  transition: 250ms ease-out;
  transform-origin: center;
  transform: scalex(0);
}
.todo-list__item-content:hover:after, .todo-list__item-content:focus:after {
  transform: scalex(1);
}
.todo-list__item-remove {
  margin-left: 0.5em;
  background: none;
  border: 1px solid;
  color: inherit;
  padding: 0;
  line-height: 1;
  width: 2em;
  height: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 80%;
}

.filters {
  width: 100%;
  display: flex;
  justify-content: space-around;
  padding: 0 1rem 1.5rem 1rem;
}

.list-move,
.list-leave-active,
.list-enter-active {
  transition: 500ms cubic-bezier(0.87, -0.41, 0.19, 1.44);
}

.list-enter,
.list-leave-active {
  transform: translate(100%, 0);
  opacity: 0;
}
</style>
