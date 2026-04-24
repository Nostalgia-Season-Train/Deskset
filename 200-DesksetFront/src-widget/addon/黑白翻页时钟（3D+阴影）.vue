<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const hourPlay2Ref = ref(null)
const hourPlayRef = ref(null)
const minutePlay2Ref = ref(null)
const minutePlayRef = ref(null)
const secondPlay2Ref = ref(null)
const secondPlayRef = ref(null)
const periodRef = ref(null)
const container = ref(null)

let timer = null

function checkTime(i) {
  if (i < 10) {
    i = "0" + i
  }
  return i
}

function checkHour(i) {
  if (i > 12) {
    i = i - 12
  }
  return checkTime(i)
}

function checkPeriod(i) {
  if (i > 12) {
    return 2
  }
  return 1
}

function setActiveElement(ulElement, index) {
  if (!ulElement) return
  const lis = ulElement.querySelectorAll('li')
  lis.forEach(li => li.classList.remove('active'))
  const targetLi = lis[index - 1]
  if (targetLi) {
    targetLi.classList.add('active')
  }
}

function initializeClock() {
  const today = new Date()
  let h = today.getHours()
  let m = today.getMinutes()
  let s = today.getSeconds()

  const p = checkPeriod(h)
  h = checkHour(h)
  m = checkTime(m)
  s = checkTime(s)

  const a = h.toString().split("")
  const h1 = parseInt(a[0]) + 1
  const h2 = parseInt(a[1]) + 1

  setActiveElement(hourPlay2Ref.value, h1)
  setActiveElement(hourPlayRef.value, h2)

  const a2 = m.toString().split("")
  const m1 = parseInt(a2[0]) + 1
  const m2 = parseInt(a2[1]) + 1

  setActiveElement(minutePlay2Ref.value, m1)
  setActiveElement(minutePlayRef.value, m2)

  const a3 = s.toString().split("")
  const s1 = parseInt(a3[0]) + 1
  const s2 = parseInt(a3[1]) + 1

  setActiveElement(secondPlay2Ref.value, s1)
  setActiveElement(secondPlayRef.value, s2)

  setActiveElement(periodRef.value, p)
}

function secondPlay() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = secondPlayRef.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    secondPlay2()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

function secondPlay2() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = secondPlay2Ref.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    minutePlay()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

function minutePlay() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = minutePlayRef.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    minutePlay2()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

function minutePlay2() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = minutePlay2Ref.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    hourPlay()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

function hourPlay() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = hourPlayRef.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    hourPlay2()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

function hourPlay2() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = hourPlay2Ref.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    period()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

function period() {
  if (!container.value) return
  container.value.classList.remove('play')

  const ul = periodRef.value
  if (!ul) return

  const aa = ul.querySelector('li.active')

  if (!aa || aa.innerHTML === "") {
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('before')
      firstLi.classList.remove('active')
      const nextLi = firstLi.nextElementSibling
      if (nextLi) {
        nextLi.classList.add('active')
      }
      if (container.value) {
        container.value.classList.add('play')
      }
    }
  }
  else if (aa === ul.lastElementChild) {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const firstLi = ul.querySelector('li')
    if (firstLi) {
      firstLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
    period()
  }
  else {
    const lis = ul.querySelectorAll('li')
    lis.forEach(li => li.classList.remove('before'))
    aa.classList.add('before')
    aa.classList.remove('active')
    const nextLi = aa.nextElementSibling
    if (nextLi) {
      nextLi.classList.add('active')
    }
    if (container.value) {
      container.value.classList.add('play')
    }
  }
}

onMounted(() => {
  initializeClock()
  timer = setInterval(() => {
    secondPlay()
  }, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>


<template>
  <div class="container" ref="container">
    <ul class="flip hourPlay2" ref="hourPlay2Ref">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
    </ul>
    <ul class="flip hourPlay" ref="hourPlayRef">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">6</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">6</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">7</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">7</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">8</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">8</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">9</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">9</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
        </a>
      </li>
    </ul>
    <span class="blinker">:</span>
    <ul class="flip minutePlay2" ref="minutePlay2Ref">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
        </a>
      </li>
    </ul>
    <ul class="flip minutePlay" ref="minutePlayRef">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">6</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">6</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">7</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">7</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">8</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">8</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">9</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">9</div>
          </div>
        </a>
      </li>
    </ul>
    <span class="blinker">:</span>
    <ul class="flip secondPlay2" ref="secondPlay2Ref">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
        </a>
      </li>
    </ul>
    <ul class="flip secondPlay" ref="secondPlayRef">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">0</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">1</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">2</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">3</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">4</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">5</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">6</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">6</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">7</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">7</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">8</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">8</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">9</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">9</div>
          </div>
        </a>
      </li>
    </ul>
    <ul class="flip period" ref="periodRef" style="transform: scale(0.5);font-size: 50px;">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">A</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">A</div>
          </div>
        </a>
      </li>
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">P</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">P</div>
          </div>
        </a>
      </li>
    </ul>

    <ul class="flip period" style="transform: scale(0.5);font-size: 50px;margin-left:-30px;">
      <li>
        <a href="#">
          <div class="up">
            <div class="shadow"></div>
            <div class="inn">M</div>
          </div>
          <div class="down">
            <div class="shadow"></div>
            <div class="inn">M</div>
          </div>
        </a>
      </li>
    </ul>
  </div>
</template>


<style scoped>
/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.blinker {
  float: left;
  font-size: 80px;
  color: #333333;
}

a {
  cursor: pointer;
  pointer-events: none;
  text-decoration: none;
  color: #ccc;
}

a:hover {
  color: #fff;
}

ul {
  list-style: none
}

.clearfix:before,
.clearfix:after {
  content: " ";
  display: table;
}

.clearfix:after {
  clear: both;
}

.clearfix {
  zoom: 1;
}

/* Main */

html,
body {
  min-height: 100%;
}

body {
  font: normal 11px "Helvetica Neue", Helvetica, sans-serif;
  user-select: none;
  color: #888;
  text-shadow: 0 1px 0 rgba(0, 0, 0, .3);
  background: rgb(150, 150, 150);
  background: -moz-radial-gradient(center, ellipse cover, rgba(150, 150, 150, 1) 0%, rgba(89, 89, 89, 1) 100%);
  background: -webkit-gradient(radial, center center, 0px, center center, 100%, color-stop(0%, rgba(150, 150, 150, 1)), color-stop(100%, rgba(89, 89, 89, 1)));
  background: -webkit-radial-gradient(center, ellipse cover, rgba(150, 150, 150, 1) 0%, rgba(89, 89, 89, 1) 100%);
  background: -o-radial-gradient(center, ellipse cover, rgba(150, 150, 150, 1) 0%, rgba(89, 89, 89, 1) 100%);
  background: -ms-radial-gradient(center, ellipse cover, rgba(150, 150, 150, 1) 0%, rgba(89, 89, 89, 1) 100%);
  background: radial-gradient(ellipse at center, rgba(150, 150, 150, 1) 0%, rgba(89, 89, 89, 1) 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#969696', endColorstr='#595959', GradientType=1);

}

.container {
  text-align: center;
  position: absolute;
  left: 0;
  top: 50%;
  right: 0;
  margin: auto;
  width: 600px;
  transform: translateY(-50%);
  height: 90px;
}

#social {
  text-align: center;
  position: absolute;
  bottom: 14%;
  width: 100%;
}

#social p {
  margin-bottom: 10px;
}

#social ul,
#social li {
  display: inline-block;
}

/* Skeleton */

ul.flip {
  position: relative;
  float: left;
  margin: 5px;
  width: 60px;
  height: 90px;
  font-size: 80px;
  font-weight: bold;
  line-height: 87px;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, .7);
}

ul.flip li {
  z-index: 1;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;

}

ul.flip li:first-child {
  z-index: 2;
}

ul.flip li a {
  display: block;
  height: 100%;
  perspective: 200px;
}

ul.flip li a div {
  z-index: 1;
  position: absolute;
  left: 0;
  width: 100%;
  height: 50%;
  overflow: hidden;
}

ul.flip li a div .shadow {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 2;
}

ul.flip li a div.up {
  transform-origin: 50% 100%;
  top: 0;
}

ul.flip li a div.up:after {
  content: "";
  position: absolute;
  top: 44px;
  left: 0;
  z-index: 5;
  width: 100%;
  height: 3px;
  background-color: rgba(0, 0, 0, .4);
}

ul.flip li a div.down {
  transform-origin: 50% 0%;
  bottom: 0;
}

ul.flip li a div div.inn {
  position: absolute;
  left: 0;
  z-index: 1;
  width: 100%;
  height: 200%;
  color: #ccc;
  text-shadow: 0 1px 2px #000;
  text-align: center;
  background-color: #333;
  border-radius: 6px;
}

ul.flip li a div.up div.inn {
  top: 0;

}

ul.flip li a div.down div.inn {
  bottom: 0;
}

/* PLAY */

.container.play ul li.before {
  z-index: 3;
}

.container.play ul li.active {
  animation: asd .5s .5s linear both;
  z-index: 2;
}

@keyframes asd {
  0% {
    z-index: 2;
  }

  5% {
    z-index: 4;
  }

  100% {
    z-index: 4;
  }
}

.container.play ul li.active .down {
  z-index: 2;
  animation: turn .5s .5s linear both;
}

@keyframes turn {
  0% {
    transform: rotateX(90deg);
  }

  100% {
    transform: rotateX(0deg);
  }
}

.container.play ul li.before .up {
  z-index: 2;
  animation: turn2 .5s linear both;
}

@keyframes turn2 {
  0% {
    transform: rotateX(0deg);
  }

  100% {
    transform: rotateX(-90deg);
  }
}

/* SHADOW */

.container.play ul li.before .up .shadow {
  background: -moz-linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(0, 0, 0, .1)), color-stop(100%, rgba(0, 0, 0, 1)));
  background: linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: -o-linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: -ms-linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: linear-gradient(to bottom, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  animation: show .5s linear both;
}

.container.play ul li.active .up .shadow {
  background: -moz-linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(0, 0, 0, .1)), color-stop(100%, rgba(0, 0, 0, 1)));
  background: linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: -o-linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: -ms-linear-gradient(top, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  background: linear-gradient(to bottom, rgba(0, 0, 0, .1) 0%, rgba(0, 0, 0, 1) 100%);
  animation: hide .5s .3s linear both;
}

/*DOWN*/

.container.play ul li.before .down .shadow {
  background: -moz-linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(0, 0, 0, 1)), color-stop(100%, rgba(0, 0, 0, .1)));
  background: linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: -o-linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: -ms-linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  animation: show .5s linear both;
}

.container.play ul li.active .down .shadow {
  background: -moz-linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(0, 0, 0, 1)), color-stop(100%, rgba(0, 0, 0, .1)));
  background: linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: -o-linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: -ms-linear-gradient(top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  background: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, .1) 100%);
  animation: hide .5s .3s linear both;
}

@keyframes show {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes hide {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}
</style>
