<template>
  <div>
    <h3>관심 장르</h3>
    <ul>
      <li v-for="genre in user.interest_genres" :key="genre">
        {{ genre }}
      </li>
    </ul>
    <h3>찜한 책</h3>
    <ul>
      <li v-for="book in user.liked_books" :key="book.id">
        {{ book.title }} - {{ book.author }}
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  user: Object
})
</script>

<style scoped>
h3 {
  margin-top: 1rem;
}
</style>
