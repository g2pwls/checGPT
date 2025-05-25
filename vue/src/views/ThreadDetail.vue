<template>
  <section class="thread-detail">
    <div class="main-container" v-if="thread">
      <div class="content-wrapper">
        <!-- 스레드 본문 및 조작 -->
        <div class="right-box">
          <h1 class="thread-title">{{ thread.title }}</h1>
          <div v-if="!isEditing">
            <p class="thread-content">{{ thread.content }}</p>
            <div class="actions" v-if="isOwnThread">
              <button @click="startEditing">수정</button>
              <button @click="deleteThread">삭제</button>
            </div>
            <div class="actions" v-if="!isOwnThread">
              <button 
                @click="toggleLike" 
                class="like-btn" 
                :class="{ 'liked': thread.is_liked }"
              >
                ❤️ {{ thread.likes_count }}
              </button>
            </div>
          </div>
          <div v-else class="edit-form">
            <input v-model="editForm.title" class="edit-input" placeholder="제목을 입력하세요" />
            <textarea v-model="editForm.content" class="edit-textarea" placeholder="내용을 입력하세요"></textarea>
            <div class="edit-actions">
              <button @click="saveEdit">저장</button>
              <button @click="cancelEdit">취소</button>
            </div>
          </div>

          <!-- 댓글 섹션 -->
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
              <div class="comment-btn-wrapper">
                <button @click="postComment" class="comment-btn">댓글 작성</button>
              </div>
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
                  <button @click="saveCommentEdit" class="save-btn">저장</button>
                  <button @click="cancelCommentEdit" class="cancel-btn">취소</button>
                </template>
                <template v-else>
                  <button @click="startCommentEdit(comment)" class="edit-btn">수정</button>
                  <button @click="deleteComment(comment.id)" class="delete-btn">삭제</button>
                </template>
              </div>
            </div>
          </div>
        </div>

        <div class="left-sidebar">
          <!-- 책 정보 -->
          <div class="left-box" v-if="thread.book">
            <RouterLink :to="{ name: 'BookDetail', params: { bookId: thread.book.id }}" class="book-card">
              <div class="book-cover">
                <img :src="thread.book.cover" alt="책 이미지" class="book-image" />
              </div>
              <div class="book-info">
                <h3 class="book-title">{{ thread.book.title }}</h3>
                <p class="book-subtitle">{{ thread.book.subTitle }}</p>
                <p class="book-author">{{ thread.book.author }}</p>
                <p class="book-pub_date">{{ thread.book.pub_date }}</p>
              </div>
            </RouterLink>
          </div>

          <!-- 프로필 정보 -->
          <div class="left-box profile-section" v-if="thread && thread.writer">
            <RouterLink 
              :to="{ name: 'UserProfile', params: { userId: thread.writer?.id } }"
              class="profile-card"
            >
              <div class="profile-image-container">
                <img
                  :src="getProfileImageUrl(thread.writer?.profile_image)"
                  alt="프로필 사진"
                  class="profile-image"
                  @error="handleImageError"
                />
              </div>
              <div class="profile-info">
                <div class="profile-name">{{ thread.writer?.name }}</div>
                <div class="profile-username">@{{ thread.writer?.username }}</div>
                <div class="follow-stats">
                  <span class="stat-item">팔로워 {{ thread.writer?.followers_count || 0 }}</span>
                  <span class="stat-divider">·</span>
                  <span class="stat-item">팔로잉 {{ thread.writer?.following_count || 0 }}</span>
                </div>
              </div>
            </RouterLink>
            <button 
              v-if="!isOwnThread" 
              @click="toggleFollow" 
              class="follow-btn" 
              :class="{ 'following': thread.writer.is_following }"
            >
              {{ thread.writer.is_following ? '팔로우 취소' : '+ 팔로우' }}
            </button>
          </div>
        </div>
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
      isEditing: false,
      editForm: {
        title: '',
        content: ''
      }
    };
  },
  computed: {
    isOwnThread() {
      const currentUserId = localStorage.getItem('userId')
      return this.thread?.writer?.id.toString() === currentUserId
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
    startCommentEdit(comment) {
      this.editingComment = { ...comment };
    },
    cancelCommentEdit() {
      this.editingComment = null;
    },
    async saveCommentEdit() {
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

        // 수정된 댓글로 업데이트
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
    startEditing() {
      this.editForm.title = this.thread.title;
      this.editForm.content = this.thread.content;
      this.isEditing = true;
    },
    cancelEdit() {
      this.isEditing = false;
      this.editForm.title = '';
      this.editForm.content = '';
    },
    async saveEdit() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.put(
          `http://127.0.0.1:8000/api/threads/${this.thread.id}/`,
          {
            title: this.editForm.title,
            content: this.editForm.content,
            book_id: this.thread.book.id
          },
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );
        
        this.thread = response.data;
        this.isEditing = false;
        this.editForm.title = '';
        this.editForm.content = '';
      } catch (error) {
        console.error('스레드 수정 실패:', error);
        alert('스레드 수정에 실패했습니다.');
      }
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
  }
}
</script>

<style scoped>
.thread-detail {
  background: #f1f1f1;
  color: black;
  padding-bottom: 40px;
  min-height: 95vh;
}

.main-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-wrapper {
  display: flex;
  flex-direction: row-reverse;
  gap: 60px;
  margin-top: 20px;
}

.right-box {
  flex: 1;
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.left-sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.left-box {
  background: white;
  padding: 25px;
  border-radius: 10px;
  width: 96%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-card {
  display: flex;
  text-decoration: none;
  color: inherit;
  gap: 15px;
  transition: transform 0.2s ease;
}

.book-card:hover {
  transform: scale(1.02);
}

.book-cover {
  width: 100px;
  flex-shrink: 0;
}

.book-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
}

.book-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.book-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.book-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.book-author {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.book-pub_date {
  font-size: 14px;
  color: #888;
  margin: 0;
}

.thread-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.thread-content {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 30px;
  color: #444;
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

.profile-section {
  height: auto;
  padding: 25px;
}

.profile-card {
  display: flex;
  text-decoration: none;
  color: inherit;
  gap: 15px;
  margin-bottom: 15px;
  width: 320px;
}

.profile-image-container {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.profile-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.profile-username {
  font-size: 14px;
  color: #666;
}

.follow-stats {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.stat-divider {
  color: #ccc;
}

.follow-btn {
  width: 100%;
  padding: 8px;
  border: none;
  border-radius: 20px;
  background: #e74c3c;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.follow-btn.following {
  background: #666;
}

.follow-btn:hover {
  background: #c0392b;
}

.follow-btn.following:hover {
  background: #555;
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
  margin: 20px 0;
}

.comment-textarea {
  width: 96%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-height: 80px;
  resize: none;
  margin-bottom: 10px;
}

.comment-btn-wrapper {
  display: flex;
  justify-content: flex-end;
}

.comment-btn {
  padding: 8px 16px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
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
  margin: 20px 0;
}

.edit-input {
  width: 96%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 18px;
}

.edit-textarea {
  width: 96%;
  min-height: 150px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  resize: vertical;
}

.edit-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: flex-end;
}

.edit-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-size: 14px;
}

.edit-actions button:first-child {
  background-color: #4CAF50;
  color: white;
}

.edit-actions button:last-child {
  background-color: #f44336;
  color: white;
}
</style>
