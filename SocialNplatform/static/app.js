document.addEventListener('click', async (ev) => {
    const likeBtn = ev.target.closest('.like-btn');
    if (likeBtn) {
      ev.preventDefault();
      const postId = likeBtn.dataset.postId;
      const res = await fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
      });
      if (res.ok) {
        const data = await res.json();
        const countEl = likeBtn.querySelector('.likes-count');
        if (countEl) countEl.textContent = data.likes_count;
      }
    }
  
    const followBtn = ev.target.closest('.follow-btn');
    if (followBtn) {
      ev.preventDefault();
      const username = followBtn.dataset.username;
      const res = await fetch(`/u/${username}/follow/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
      });
      if (res.ok) {
        const data = await res.json();
        followBtn.textContent = data.following ? 'Unfollow' : 'Follow';
        const followersText = document.querySelector('.profile-header p');
        if (followersText && data.followers_count !== undefined) {
          // naive update: reload to reflect counts accurately
          location.reload();
        }
      }
    }
  });
  
  function getCSRFToken() {
    const name = 'csrftoken=';
    const parts = document.cookie.split(';');
    for (const p of parts) {
      const s = p.trim();
      if (s.startsWith(name)) return s.substring(name.length);
    }
    const el = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return el ? el.value : '';
  }
  
  