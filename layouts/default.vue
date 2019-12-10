<template>
  <div class="columns">
    <aside class="section menu column is-narrow has-background-light">
      <p class="menu-label">General</p>
      <ul class="menu-list">
        <li>
          <nuxt-link to="/">Home</nuxt-link>
        </li>
        <li>
          <nuxt-link to="/conceal">Data concealing</nuxt-link>
        </li>
        <li>
          <nuxt-link to="/reveal">Data revealing</nuxt-link>
        </li>
      </ul>
      <p class="menu-label">Resources</p>
      <ul class="menu-list">
        <li>
          <a href="https://github.com/lqmanh/steganopy">Github</a>
        </li>
      </ul>
      <p class="menu-label">Authors</p>
      <ul class="menu-list">
        <li>
          <a href="https://github.com/lqmanh">Lương Quang Mạnh</a>
        </li>
        <li>
          <a href="https://github.com/nghiaduy9">Ngô Đức Nghĩa</a>
        </li>
      </ul>
    </aside>
    <div class="column">
      <nuxt />
    </div>
  </div>
</template>

<style scoped>
.columns {
  height: 100vh;
  width: 100vw;
}
</style>
