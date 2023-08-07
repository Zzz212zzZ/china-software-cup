<template>
  <footer class="footer">
    <div class="container-fluid d-flex flex-wrap justify-content-between">
      <nav>
        <ul>
          <li>
            <router-link :to="{ path: '/admin' }">Dashboard</router-link>
          </li>
        </ul>
      </nav>
      <div class="copyright d-flex flex-wrap">
        &copy; Code uploaded in
        <!-- <i class="fa fa-heart heart"></i> -->
        
        <a href="https://gitee.com/zzz212zzz/sftcup" target="_blank">
          &nbsp; Gitee Repository
          <i class="fa fa-brands fa-git" style="color: #74c4d0;"></i>
        
        </a>&nbsp; for the
        <a href="https://aistudio.baidu.com/aistudio/competition/detail/887/0/introduction" target="_blank">&nbsp; "China
          Software Cup" Design Competition
          <i class="fa fa-solid fa-bolt fa-beat" style="color: #6bc1d6;"></i>
        </a>
      </div>
    </div>

  </footer>
</template>
<script>
export default {};
</script>
<style></style>
