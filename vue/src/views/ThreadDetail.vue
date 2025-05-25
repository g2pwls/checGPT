<template>
  <section class="thread-detail">
    <div class="main-container" v-if="thread">
      <!-- 책 정보 -->
      <div class="left-box" v-if="thread.book">
        <RouterLink :to="{ name: 'BookDetail', params: { bookId: thread.book.id }}">
          <img :src="thread.book.cover" alt="책 이미지" class="book-image" />
          <div class="book-info">
            <div class="book-title">{{ thread.book.title }}</div>
            <div class="book-subtitle">{{ thread.book.subTitle }}</div>
            <div class="book-pub_date">{{ thread.book.pub_date }}</div>
          </div>
        </RouterLink>
      </div>

      <!-- 스레드 본문 및 조작 -->
      <div class="right-box">
        <h1 class="thread-title">{{ thread.title }}</h1>
        <p class="thread-content">{{ thread.content }}</p>
        <div class="actions">
          <button 
            @click="toggleLike" 
            class="like-btn" 
            :class="{ 'liked': thread.is_liked }"
          >
            ❤️ {{ thread.likes_count }}
          </button>
          <button @click="editThread">수정</button>
          <button @click="deleteThread">삭제</button>
        </div>

        <!-- 댓글 -->
        <div class="comments" v-if="thread.comments">
          <h3>댓글 ({{ thread.comments_count }})</h3>
          <div class="comment-input-section">
            <textarea 
              v-model="newComment" 
              placeholder="댓글을 입력하세요..." 
              id="comment-input"
              name="comment-input"
              @keyup.enter="postComment"
              @input="autoResize"
              ref="commentInput"
              class="comment-textarea"
            ></textarea>
            <button @click="postComment" class="comment-btn">댓글 작성</button>
          </div>

          <div v-for="comment in thread.comments" :key="comment.id" class="comment">
            <div class="comment-content">
              <div v-if="editingComment?.id === comment.id" class="edit-form">
                <textarea 
                  v-model="editingComment.content" 
                  class="edit-textarea"
                  rows="2"
                ></textarea>
              </div>
              <p v-else>{{ comment.content }}</p>
              <div class="comment-meta">
                <span class="comment-author">@{{ comment.author.username }}</span>
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              </div>
            </div>
            <div class="comment-actions" v-if="isCommentAuthor(comment)">
              <template v-if="editingComment?.id === comment.id">
                <button @click="saveEdit" class="save-btn">저장</button>
                <button @click="cancelEdit" class="cancel-btn">취소</button>
              </template>
              <template v-else>
                <button @click="startEdit(comment)" class="edit-btn">수정</button>
                <button @click="deleteComment(comment.id)" class="delete-btn">삭제</button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 프로필 정보 -->
    <div class="profile-box" v-if="thread && thread.writer">
      <div class="thread-header">
        <div class="user-info">
          <RouterLink 
            :to="{ name: 'UserProfile', params: { userId: thread.writer?.id } }"
            class="profile-image-link"
          >
            <img
              :src="getProfileImageUrl(thread.writer?.profile_image)"
              alt="프로필 사진"
              class="profile-image"
              @error="handleImageError"
            />
          </RouterLink>
          <div class="user-details">
            <RouterLink 
              :to="{ name: 'UserProfile', params: { userId: thread.writer?.id } }"
              class="username-link"
            >
              {{ thread.writer?.name }} 
            </RouterLink>
            <RouterLink 
              :to="{ name: 'UserProfile', params: { userId: thread.writer?.id } }"
              class="username"
            >
              @{{ thread.writer?.username }} 
            </RouterLink>
          </div>
        </div>
        <div class="follow-stats">
          <div class="stat-item">
            <span class="stat-value">{{ thread.writer?.followers_count || 0 }}</span>
            <span class="stat-label">팔로워</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ thread.writer?.following_count || 0 }}</span>
            <span class="stat-label">팔로잉</span>
          </div>
        </div>
        <button 
          v-if="!isOwnThread" 
          @click="toggleFollow" 
          class="follow-btn" 
          :class="{ 'following': thread.writer.is_following }"
          id="follow-button"
          name="follow-button"
        >
          {{ thread.writer.is_following ? '팔로우 취소' : '+ 팔로우' }}
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      thread: null,
      newComment: '',
      editingComment: null,
    };
  },
  computed: {
    isOwnThread() {
      const currentUserId = localStorage.getItem('userId')
      return this.thread?.writer?.id === currentUserId
    }
  },
  async mounted() {
    try {
      const id = this.$route.params.threadId;
      const token = localStorage.getItem('token');

      // Load thread data
      const res = await axios.get(`http://127.0.0.1:8000/api/threads/${id}/`, {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      this.thread = res.data;

      // Check follow status and get counts
      if (this.thread.writer) {
        try {
          // Get user profile to get follower/following counts and follow status
          const profileRes = await axios.get(
            `http://127.0.0.1:8000/accounts/api/users/${this.thread.writer.id}/profile/`,
            {
              headers: {
                Authorization: `Token ${token}`
              }
            }
          );
          this.thread.writer.is_following = profileRes.data.is_following;
          this.thread.writer.followers_count = profileRes.data.followers_count;
          this.thread.writer.following_count = profileRes.data.following_count;
        } catch (error) {
          console.error('Profile data check failed:', error);
        }
      }
    } catch (err) {
      console.error('데이터 로딩 실패:', err);
    }
  },
  methods: {
    async toggleLike() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('로그인이 필요합니다.');
          return;
        }

        // Optimistically update UI
        const newLikeStatus = !this.thread.is_liked;
        this.thread.is_liked = newLikeStatus;
        this.thread.likes_count += newLikeStatus ? 1 : -1;

        const response = await axios.post(
          `http://127.0.0.1:8000/api/threads/${this.thread.id}/like/`,
          {},
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );

        // Update with server response
        this.thread.is_liked = response.data.is_liked;
        this.thread.likes_count = response.data.likes_count;
      } catch (error) {
        console.error("좋아요 토글 실패:", error);
        // Revert optimistic update on error
        this.thread.is_liked = !this.thread.is_liked;
        this.thread.likes_count += this.thread.is_liked ? 1 : -1;

        if (error.response) {
          if (error.response.status === 401) {
            alert('로그인이 필요합니다.');
          } else {
            alert('좋아요 처리에 실패했습니다.');
          }
        }
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      
      return `${year}/${month}/${day} ${hours}:${minutes}`;
    },
    isCommentAuthor(comment) {
      const currentUserId = localStorage.getItem('userId');
      return comment.author.id.toString() === currentUserId;
    },
    autoResize(event) {
      const textarea = event.target;
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
    },
    async postComment() {
      if (!this.newComment.trim()) {
        alert('댓글 내용을 입력해주세요.');
        return;
      }

      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('로그인이 필요합니다.');
          return;
        }

        const response = await axios.post(
          `http://127.0.0.1:8000/api/comments/`,
          {
            thread: this.thread.id,
            content: this.newComment,
          },
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );

        // Add the new comment to the list
        this.thread.comments.unshift(response.data);
        this.thread.comments_count += 1;
        this.newComment = '';
        // Reset textarea height after posting
        if (this.$refs.commentInput) {
          this.$refs.commentInput.style.height = 'auto';
        }
      } catch (error) {
        console.error('댓글 작성 실패:', error);
        if (error.response?.status === 401) {
          alert('로그인이 필요합니다.');
        } else {
          alert('댓글 작성에 실패했습니다.');
        }
      }
    },
    startEdit(comment) {
      this.editingComment = { ...comment };
    },
    cancelEdit() {
      this.editingComment = null;
    },
    async saveEdit() {
      if (!this.editingComment.content.trim()) {
        alert('댓글 내용을 입력해주세요.');
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const response = await axios.put(
          `http://127.0.0.1:8000/api/comments/${this.editingComment.id}/`,
          {
            content: this.editingComment.content,
            thread: this.thread.id
          },
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );

        // Update the comment in the list
        const index = this.thread.comments.findIndex(c => c.id === this.editingComment.id);
        if (index !== -1) {
          this.thread.comments[index] = response.data;
        }
        this.editingComment = null;
      } catch (error) {
        console.error('댓글 수정 실패:', error);
        if (error.response?.data) {
          console.error('Error details:', error.response.data);
        }
        alert('댓글 수정에 실패했습니다.');
      }
    },
    async deleteComment(commentId) {
      if (!confirm('댓글을 삭제하시겠습니까?')) return;

      try {
        const token = localStorage.getItem('token');
        await axios.delete(
          `http://127.0.0.1:8000/api/comments/${commentId}/delete/`,
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );

        // Remove the comment from the list
        this.thread.comments = this.thread.comments.filter(c => c.id !== commentId);
        this.thread.comments_count -= 1;
      } catch (error) {
        console.error('댓글 삭제 실패:', error);
        alert('댓글 삭제에 실패했습니다.');
      }
    },
    async editThread() {
      this.$router.push(`/threads/${this.thread.id}/edit`);
    },
    async deleteThread() {
      try {
        const token = localStorage.getItem('token'); // 로그인 시 저장한 토큰 불러오기
        await axios.delete(`http://127.0.0.1:8000/api/threads/${this.thread.id}/`, {
          headers: {
            Authorization: `Token ${token}`
          }
        });
        this.$router.push(`/books/${this.thread.book.id}`);
      } catch (error) {
        console.error('삭제 실패:', error);
      }
    },
    async toggleFollow() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('로그인이 필요합니다.');
          return;
        }

        // Check if trying to follow self
        const currentUserId = localStorage.getItem('userId');
        if (currentUserId === this.thread.writer.id.toString()) {
          alert('자기 자신을 팔로우할 수 없습니다.');
          return;
        }

        // Optimistically update UI
        const newFollowStatus = !this.thread.writer.is_following;
        this.thread.writer.is_following = newFollowStatus;
        this.thread.writer.followers_count += newFollowStatus ? 1 : -1;

        const response = await axios.post(
          `http://127.0.0.1:8000/accounts/api/follow/${this.thread.writer.id}/`,
          {},
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );

        // Refresh profile data to get updated counts
        const profileRes = await axios.get(
          `http://127.0.0.1:8000/accounts/api/users/${this.thread.writer.id}/profile/`,
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );

        // Update with fresh data from server
        this.thread.writer.is_following = profileRes.data.is_following;
        this.thread.writer.followers_count = profileRes.data.followers_count;
        this.thread.writer.following_count = profileRes.data.following_count;

        // Force Vue to recognize the changes
        this.thread = { ...this.thread };
      } catch (error) {
        console.error("팔로우 토글 실패:", error);
        // Revert optimistic update on error
        this.thread.writer.is_following = !this.thread.writer.is_following;
        this.thread.writer.followers_count += this.thread.writer.is_following ? 1 : -1;
        this.thread = { ...this.thread };

        if (error.response) {
          console.error("Error response:", error.response.data);
          if (error.response.status === 400) {
            alert(error.response.data.error || '팔로우할 수 없습니다.');
          } else if (error.response.status === 401) {
            alert('로그인이 필요합니다.');
          }
        }
      }
    },
    getProfileImageUrl(imagePath) {
      if (!imagePath) return '/default-profile.png'
      // If the image path is already a full URL, return it as is
      if (imagePath.startsWith('http')) return imagePath
      // Otherwise, prepend the Django media URL
      return `http://127.0.0.1:8000${imagePath}`
    },
    handleImageError(e) {
      console.log('Image load error, using default image')
      e.target.src = '/default-profile.png'
    },
  }
}
</script>

<style scoped>
.thread-detail {
  background: #f1f1f1;
  color: black;
  padding-bottom: 40px;
  height: 95vh;
}

/* 가운데 정렬 */
.main-container {
  display: flex;
  padding: 20px;
  gap: 40px;
  max-width: 1000px;
  margin: 0 auto;
}

.left-box {
  background: #222;
  padding: 20px;
  border-radius: 10px;
  width: 260px;
}

.left-box a {
  text-decoration: none;
  color: inherit;
  display: block;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.left-box a:hover {
  transform: scale(1.02);
}

.book-image {
  width: 100%;
  border-radius: 6px;
  margin-bottom: 10px;
}

.book-title {
  font-size: 20px;
  font-weight: bold;
  color: #f1f1f1;
}
.book-subtitle {
  font-size: 14px;
  color: #aaa;
}
.book-pub_date {
  font-size: 14px;
  color: #aaa;
}

.right-box {
  flex: 1;
}
.thread-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 10px;
}
.thread-content {
  font-size: 16px;
  margin-bottom: 20px;
}
.actions button {
  margin-right: 10px;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
}
.actions-comment button {
  display: flex;
  margin-right: 10px;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
}
.comments {
  margin-top: 40px;
}
.comments input {
  width: 80%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
  border: none;
  border: 1px solid #cecece;
}
.comment {
  background: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  width: 100%;
  box-sizing: border-box;
}

.profile-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px;
  margin: 20px auto;
  background: #1c1c1c;
  border-top: 1px solid #333;
  max-width: 1000px;
}
.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.username {
  color: #aaa;
  text-decoration: none;
  font-size: 0.9em;
  transition: color 0.3s ease;
}
.username:hover {
  color: #e74c3c;
}
.follow-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
}
.following {
  background: #333;
}

.thread-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-image {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 50%;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-image-link {
  display: block;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.profile-image-link:hover {
  transform: scale(1.05);
}

.username-link {
  color: #f1f1f1;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1em;
  transition: color 0.3s ease;
}

.username-link:hover {
  color: #e74c3c;
}

.follow-stats {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
}

.stat-label {
  font-size: 14px;
  color: #aaa;
}

.follow-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.follow-btn:hover {
  background: #c0392b;
}

.following {
  background: #333;
}

.following:hover {
  background: #444;
}

.like-btn {
  margin-right: 10px;
  background: #f0f0f0;
  color: #333;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-btn.liked {
  background: #e74c3c;
  color: white;
}

.like-btn:hover {
  transform: scale(1.05);
}

.comment-input-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
}

.comment-textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-height: 40px;
  max-height: 200px;
  resize: none;
  overflow-y: auto;
  line-height: 1.4;
  box-sizing: border-box;
  transition: height 0.1s ease;
}

.comment-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.comment-btn {
  padding: 10px 20px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  align-self: flex-start;
  white-space: nowrap;
}

.comment-btn:hover {
  background: #c0392b;
}

.comment-content {
  margin-bottom: 10px;
  width: 100%;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #666;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  color: #999;
}

.comment-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.edit-btn, .delete-btn, .save-btn, .cancel-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s;
}

.edit-btn {
  background: #3498db;
  color: white;
}

.edit-btn:hover {
  background: #2980b9;
}

.delete-btn {
  background: #e74c3c;
  color: white;
}

.delete-btn:hover {
  background: #c0392b;
}

.save-btn {
  background: #2ecc71;
  color: white;
}

.save-btn:hover {
  background: #27ae60;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
}

.cancel-btn:hover {
  background: #7f8c8d;
}

.edit-form {
  margin-bottom: 10px;
  width: 100%;
  box-sizing: border-box;
}

.edit-textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 8px;
  font-size: 14px;
  resize: none;
  min-height: 40px;
  max-height: 100px;
  overflow-y: auto;
  box-sizing: border-box;
  line-height: 1.4;
}
</style>
