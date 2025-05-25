<template>
  <div class="profile-container">
    <div class="content-wrapper">
      <!-- Left Sidebar -->
      <div class="left-sidebar">
        <div class="profile-box">
          <img 
            :src="getProfileImageUrl(user.profile_image)" 
            alt="프로필 사진" 
            class="profile-image"
            @error="handleImageError"
          />
          <h2 class="profile-name">{{ user.name }}</h2>
          <p class="profile-username">@{{ user.username }}</p>
          <div class="follow-stats">
            <div class="stat">
              <span class="stat-value">{{ user.followers_count || 0 }}</span>
              <span class="stat-label">팔로워</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.following_count || 0 }}</span>
              <span class="stat-label">팔로잉</span>
            </div>
          </div>
          <button 
            v-if="!isOwnProfile" 
            @click="toggleFollow" 
            :class="['follow-button', { 'following': user.is_following }]"
          >
            {{ user.is_following ? '팔로우 취소' : '+ 팔로우' }}
          </button>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-box">
        <div class="tabs">
          <button 
            @click="activeTab = 'library'" 
            :class="['tab-button', { active: activeTab === 'library' }]"
          >
            {{ user.name }}님의 서재
          </button>
          <button 
            @click="activeTab = 'threads'" 
            :class="['tab-button', { active: activeTab === 'threads' }]"
          >
            {{ user.name }}님의 스레드
          </button>
        </div>

        <div class="tab-content">
          <!-- Library Tab -->
          <div v-if="activeTab === 'library'" class="library-content">
            <div v-if="library.length === 0" class="empty-state">
              <p>서재에 추가된 책이 없습니다.</p>
            </div>
            <div v-else class="library-grid">
              <div v-for="item in library" :key="item.id" class="library-item" @click="goToBook(item.book.id)">
                <img :src="item.book.cover" :alt="item.book.title" class="book-cover">
                <h3 class="book-title">{{ item.book.title }}</h3>
                <p class="book-author">{{ item.book.author }}</p>
              </div>
            </div>
          </div>

          <!-- Threads Tab -->
          <div v-if="activeTab === 'threads'" class="threads-content">
            <div v-if="threads.length === 0" class="empty-state">
              <p>작성한 스레드가 없습니다.</p>
            </div>
            <div v-else class="threads-list">
              <div v-for="thread in threads" :key="thread.id" class="thread-item" @click="goToThread(thread.id)">
                <div class="thread-main">
                  <h3 class="thread-title">{{ thread.title }}</h3>
                  <p class="thread-content">{{ thread.content }}</p>
                </div>
                <div class="thread-footer">
                  <div class="thread-book-info">
                    <img 
                      :src="thread.book.cover" 
                      :alt="thread.book.title" 
                      class="thread-book-cover"
                      @error="handleImageError"
                    />
                    <span class="thread-book-title">{{ thread.book.title }}</span>
                  </div>
                  <span class="thread-date">{{ formatDate(thread.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const user = ref({})
const threads = ref([])
const library = ref([])
const isFollowing = ref(false)
const activeTab = ref('library')

// Check if this is the user's own profile
const isOwnProfile = computed(() => {
  const currentUserId = localStorage.getItem('userId')
  return !route.params.userId || route.params.userId === currentUserId
})

const getProfileImageUrl = (imagePath) => {
  if (!imagePath) return '/default-profile.png'
  if (imagePath.startsWith('http')) return imagePath
  return `http://127.0.0.1:8000${imagePath}`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return ''
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    
    return `${year}/${month}/${day} ${hours}:${minutes}`
  } catch (error) {
    console.error('Date formatting error:', error)
    return ''
  }
}

const loadProfileData = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const userId = route.params.userId
    console.log('Current route userId:', userId)
    
    const endpoint = `http://127.0.0.1:8000/accounts/api/users/${userId}/profile/`
    
    console.log('Loading profile from:', endpoint)
    const res = await axios.get(endpoint, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log('Profile response:', res.data)
    
    if (res.data) {
      user.value = res.data
      console.log('User value after setting:', user.value)
      isFollowing.value = user.value.is_following

      if (user.value.id) {
        console.log('User ID found:', user.value.id)
        try {
          // Load user's library
          const libraryEndpoint = `http://127.0.0.1:8000/api/users/${userId}/library/`
          console.log('Loading library from:', libraryEndpoint)
          
          try {
            const libraryRes = await axios.get(libraryEndpoint, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
            console.log('Library response:', libraryRes)
            library.value = libraryRes.data
          } catch (error) {
            console.error('Library loading error:', error)
            library.value = []
          }

          // Load user's threads
          try {
            const threadsEndpoint = `http://127.0.0.1:8000/api/users/${userId}/threads/`
            console.log('Loading threads from:', threadsEndpoint)
            const threadsRes = await axios.get(threadsEndpoint, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
            console.log('Threads response:', threadsRes.data)
            threads.value = threadsRes.data
          } catch (error) {
            console.error('Error loading threads:', error)
            threads.value = []
          }
        } catch (error) {
          console.error('Error loading user data:', error)
        }
      }
    } else {
      console.error('No user data received')
      user.value = {}
      threads.value = []
      library.value = []
    }
  } catch (error) {
    console.error("프로필 로딩 실패:", error)
    if (error.response) {
      if (error.response.status === 401) {
        router.push('/login')
      } else {
        user.value = {}
        threads.value = []
        library.value = []
      }
    }
  }
}

const handleImageError = (e) => {
  console.log('Image load error, using default image')
  e.target.src = '/default-profile.png'
}

const toggleFollow = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('로그인이 필요합니다.')
      return
    }

    const currentUserId = localStorage.getItem('userId')
    if (currentUserId === route.params.userId) {
      alert('자기 자신을 팔로우할 수 없습니다.')
      return
    }

    const newFollowStatus = !user.value.is_following
    user.value.is_following = newFollowStatus
    user.value.followers_count += newFollowStatus ? 1 : -1

    const response = await axios.post(
      `http://127.0.0.1:8000/accounts/api/follow/${route.params.userId}/`,
      {},
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    const profileRes = await axios.get(
      `http://127.0.0.1:8000/accounts/api/users/${route.params.userId}/profile/`,
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    user.value = profileRes.data
    user.value = { ...user.value }
  } catch (error) {
    console.error("팔로우 토글 실패:", error)
    user.value.is_following = !user.value.is_following
    user.value.followers_count += user.value.is_following ? 1 : -1
    user.value = { ...user.value }

    if (error.response) {
      if (error.response.status === 400) {
        alert(error.response.data.error || '팔로우할 수 없습니다.')
      } else if (error.response.status === 401) {
        alert('로그인이 필요합니다.')
      }
    }
  }
}

const goToThread = (threadId) => {
  router.push(`/threads/${threadId}`)
}

const goToBook = (bookId) => {
  router.push(`/books/${bookId}`)
}

onMounted(() => {
  loadProfileData()
})

watch(
  () => route.params.userId,
  (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
      loadProfileData()
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 2rem;
}

.left-sidebar {
  width: 300px;
  flex-shrink: 0;
}

.profile-box {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 1rem;
  object-fit: cover;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.profile-username {
  color: #666;
  margin-bottom: 1rem;
}

.follow-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.follow-button {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 0.5rem;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.follow-button:hover {
  background-color: #0056b3;
}

.follow-button.following {
  background-color: #6c757d;
}

.follow-button.following:hover {
  background-color: #5a6268;
}

.right-box {
  flex: 1;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 0 1rem;
}

.tab-button {
  padding: 1rem 1.5rem;
  border: none;
  background: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.tab-button:hover {
  color: #333;
}

.tab-button.active {
  color: #007bff;
  font-weight: bold;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #007bff;
}

.tab-content {
  padding: 2rem;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.library-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.library-item {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: transform 0.2s;
  cursor: pointer;
}

.library-item:hover {
  transform: translateY(-2px);
}

.book-cover {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}

.book-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #333;
}

.book-author {
  font-size: 0.9rem;
  color: #666;
}

.threads-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.thread-item {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: transform 0.2s;
  cursor: pointer;
}

.thread-item:hover {
  transform: translateY(-2px);
}

.thread-main {
  margin-bottom: 1rem;
}

.thread-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.thread-content {
  color: #666;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.thread-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.thread-book-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.thread-book-cover {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 0.25rem;
}

.thread-book-title {
  color: #666;
  font-size: 0.9rem;
}

.thread-date {
  color: #888;
  font-size: 0.9rem;
}
</style>
