const currentUser = document.querySelector("#loggedin-user").value;

document.addEventListener('DOMContentLoaded', () => {
    // Select edit post button
    document.querySelector(".edit-post").addEventListener("click", getPostId);
    // Select like post button
    document.querySelector(".like-post").addEventListener("submit", likePost);
});


// Get post id when the edit button is pressed
const getPostId = post_id => {
    const postId = post_id.value;
    // Show/hide DOM elements
    document.querySelector(`#post-body-${postId}`).style.display = "none";
    document.querySelector(`#edit-post-${postId}`).style.display = "none";
    document.querySelector(`#save-post-${postId}`).style.display = "block";
    document.querySelector(`#save-post-${postId}`).addEventListener("submit", () => editUserPost(postId));
};


// Write the fetch method to like/unlike posts and pass above button to
const likePost = post_id => {
  event.preventDefault();
  const likeId = parseInt(post_id.name);
  const likeURL = `/like/${likeId}`;
  let numLikes = document.querySelector(`#likes-${likeId}`);
  const csrftoken = getCookie('csrftoken');
  
  fetch(likeURL, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken,
      },
    })
    .then(response => response.json())
    .then(data => {
      numLikes.innerHTML = `${data.likes} Likes`;
  })
  .catch(error => {
    console.log("Error", error);
  });
};


const editUserPost = post_id => {
  event.preventDefault();
  // Set query selectors for bio and website
  const body = document.querySelector(`#compose-body-${post_id}`).value;
  const postBody = document.querySelector(`#post-body-${post_id}`);
  const savePost = document.querySelector(`#save-post-${post_id}`);
  const editButton = document.querySelector(`#edit-post-${post_id}`);
  
  let message = document.querySelector(`#message-${post_id}`);
  const editURL = `/updatepost/${post_id}`;
  const csrftoken = getCookie('csrftoken');
  
  const bodyData = {
    body
  };
  
  fetch(editURL, {
    method: 'PUT',
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(bodyData)
  })
    .then(response => response.json())
    .then(data => {
      postBody.innerHTML = bodyData.body;
      
      savePost.style.display = "none";
      editButton.style.display = "block";
      postBody.style.display = "block";
      message.style.display = "block";
      
      message.innerHTML = "Post updated.";
      
      // Show   post saved message for 3 seconds
      setTimeout(() => { 
        message.innerHTML = '';
        message.style.display = "none";
      }, 3000);
    })
    .catch(error => {
      console.log('Error', error);
    });
  return false;
};


// Cookie handler from Django docs
const getCookie = name => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
