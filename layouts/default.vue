<template>
  <div class="columns">
    <aside class="section menu column is-narrow has-background-light">
      <p class="menu-label">General</p>
      <ul class="menu-list">
        <li>
          <nuxt-link to="/">
            <ion-icon name="home" />
            &nbsp;Home
          </nuxt-link>
        </li>
        <li>
          <nuxt-link to="/conceal">
            <ion-icon name="eye-off" />
            &nbsp;Data concealing
          </nuxt-link>
        </li>
        <li>
          <nuxt-link to="/reveal">
            <ion-icon name="eye" />
            &nbsp;Data revealing
          </nuxt-link>
        </li>
      </ul>
      <p class="menu-label">Resources</p>
      <ul class="menu-list">
        <li>
          <a href="https://github.com/lqmanh/steganopy">
            <ion-icon name="logo-github" />
            &nbsp;Github
          </a>
        </li>
      </ul>
      <p class="menu-label">Authors</p>
      <ul class="menu-list">
        <li>
          <a href="https://github.com/lqmanh">
            <ion-icon name="person"></ion-icon>
            &nbsp;Lương Quang Mạnh
          </a>
        </li>
        <li>
          <a href="https://github.com/nghiaduy9">
            <ion-icon name="person"></ion-icon>
            &nbsp;Ngô Đức Nghĩa
          </a>
        </li>
      </ul>
    </aside>
    <div class="section column">
      <nuxt />
    </div>
  </div>
</template>

<style scoped>
.columns {
  height: 100vh;
  width: 100vw;
}
.section {
  padding: 3rem 2rem;
}
</style>
