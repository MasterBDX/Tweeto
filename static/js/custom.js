

// Function that get parameters using name //
function getParameterByName(name, url) {
  if (!url) url = window.location.href
  name = name.replace(/[\[\]]/g, '\\$&')
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)')
  var results = regex.exec(url)
  if (!results) return null
  if (!results[2]) return ''
  return decodeURIComponent(results[2].replace(/\+/g, ' '))
}
// ----------------------------------------------------------

function loadTweetsContainer(containerID, featchOneID) {
  const query = getParameterByName('q')
  let tweetList = []
  let nextUrl;
  let tweetsContainer = $('#tweets');

  if (containerID) {
    tweetsContainer = $('#' + containerID)
  }
  let fetchUrl = tweetsContainer.attr('data-url') || '/api/tweets/';

  function updateHashLinks() {
    $('.tweetBody p').each(function (data) {

      const regex = /(^|\s)#([\w\d-]+)/g
      const regex2 = /(^|\s)@([\w\d-]+)/g
      let currentHtml = $(this).html();
      const html = `
                       $1<a href='/hashtag/$2/'>#$2</a>
                     `
      const html2 = `
                        $1<a href='/$2/'>@$2</a>
                      `
      let newText;

      newText = currentHtml.replace(regex, html)
      newText = newText.replace(regex2, html2)
      $(this).html(newText)
    })
  }

  /* function that add our Tweet function that return your
    name either append or prepend */
  function tweetFormat(value) {
    let tweet = {
      url: value.url,
      dateDisplay: value.display_date,
      username: value.user.username,
      content: value.content,
      id: value.id,
      real_id: value.id,
      likesNum: value.likes_num,
      is_like: value.is_like,
      reply: value.reply,
      image: value.image,
      myTweet: value.my_tweet,
      avatar: value.user.avatar
    }

    let avatar = `<i class="fas fa-user fa-2x"></i>`;
    if (tweet.avatar) {
      avatar = `<img src='${tweet.avatar}' />`

    }
    let usernameCapitalized = tweet.username.charAt(0).toUpperCase() + tweet.username.slice(1);
    let isRetweet = `<div class="col text-center"> 
                    <a href='/tweets/${tweet.id}/retweet/' 
                       class='btn btn-link retweet-anchor'>
                       <i class="fas fa-retweet"></i> 
                    </a>
                    </div>`
    let image = '';

    let like;

    if (tweet.is_like == 'Unliked') {
      like = `<i data-id='${tweet.real_id}' 
              class="fas fa-thumbs-up "></i>`
    } else {
      like = `<i data-id='${tweet.real_id}' 
              class="far fa-thumbs-up"></i>`
    }
    let myTweet = '';

    if (tweet.myTweet) {
      myTweet = ` 
                  <button 
                      class='btn delete-btn'
                      data-id='${tweet.real_id}'
                      data-arrow="right"
                      >
                      Delete Tweet&nbsp;
                      <i class="fas fa-chevron-right"></i>
                  </button>

                  `
    }
    if (tweet.image) {
      image = `
            <div class='tweet-image-container'> 
                <img class='tweet-image' src="${tweet.image}" />
            </div>`
    }

    if (value.parent && !value.reply) {
      usernameCapitalized = ` Retweeted via ${usernameCapitalized} `
      isRetweet = '';
      tweet.content = value.parent.content;
      tweet.id = value.parent.id;
      tweet.likesNum = value.parent.likes_num

    } else if (value.parent && value.reply) {
      tweet.id = value.parent.id;
      isRetweet = '';
      let html_ = `
                     
                    <a class='reply-user' href="${tweet.url}">
                      ${usernameCapitalized}
                    </a> 
                  `
      usernameCapitalized = html_;
    }

    const html_ = `
    <section id="tweet">
      <a href="/tweets/${tweet.id}">
      <div class="tweet-body tweetBody">
      <div class="tweet-header"> 
          ${image}
      </div>
          <p class="lead tweet-content">
            ${tweet.content}
          </p>
        </a>
        <div class="tweet-btns">
          <div class="row">
            
            
              ${isRetweet}
            

            <div class="col text-center">
              <a class='reply-btn btn-link' href="" data-id='${tweet.id}' 
                data-user="${tweet.username}" >
                <i class="fas fa-reply"></i>
              </a>
            </div>

            <div class="col text-center">
              <a 
                class='like-btn btn-link' 
                data-id='${tweet.real_id}' 
                href="">
                ${like}
              </a>
              <span id='likes-num-${tweet.real_id}'> ${tweet.likesNum}</span>
            </div>

          </div>
        </div>

          <div id='tweet-${tweet.real_id}'></div>

          <div class="user-info"> 
                <a href = "${tweet.url}" class=" btn-link" >
                  <div 
                    class='user-tweet-avatar'>
                      ${avatar}
                  </div> 
                
                  ${usernameCapitalized}
                
                </a>
                <span>${tweet.dateDisplay}</span>
                </div>
         
          ${myTweet}

          <div class='delete-tweet-div' id="delete-tweet-form-${tweet.real_id}">
              <form  
                  action='/api/tweets/${tweet.real_id}/delete/'
                  id="delete-tweet-form"
              >
                <br />
                <div class="alert alert-warning" role="alert">
                  Are you sure you want to delete this tweet ?
                </div>
                <button class='btn confirm-delete-btn' type="submit">
                  <i class="far fa-trash-alt"></i> Delete
                </button>
              </form>
            </div>
          <hr />
          </section>
          `
    return html_
  }

  function attachTweet(value, prepend) {
    tweet = tweetFormat(value)
    if (prepend == true) {
      $('#no-tweets-msg').remove();
      tweetsContainer.prepend(tweet)
    } else {
      tweetsContainer.append(tweet)
    }
  }
  // --------------------------------------------------

  // function that parse our tweets //
  function parseTweets() {
    if (tweetList == 0) {
      tweetsContainer.html('<h1 id="no-tweets-msg">No Tweets currently found</h1>')
    } else {
      $.each(tweetList, (key, value) => {
        const tweetKey = key
        attachTweet(value)
      })
    }
  }

  //-------- function that featch our tweets ---------------  //

  function tweetsFetcher(url) {
    let fetcherUrl;
    if (!url) {
      fetcherUrl = fetchUrl
    } else {
      fetcherUrl = url
    }
    $.ajax({
      url: fetcherUrl,
      method: 'GET',
      data: { q: query },
      success: function (data) {
        console.log('success')
        tweetList = data.results
        if (data.next) {
          nextUrl = data.next;

        } else {
          $('#load-more-btn').css('display', 'none')
        }
        parseTweets()
        updateHashLinks()
        $('#load-more-btn').text('Load more')

      },
      error: function (error) {
        console.log(error.status)
        if (error.status == 403) {
          window.location.href = '/account/login'
        }
      }

    })
  }
  //-------------------------------------------------------//

  //-------- function that featch a single Tweet ---------------  //

  function tweetFetcher(featchOneID) {
    $.ajax({
      url: '/api/tweets/' + featchOneID + '/',
      method: 'GET',
      success: (data) => {
        console.log(data)
        tweetList = data.results
        parseTweets()
        updateHashLinks()

      },
      error: (errors) => {
        console.log(errors.status)
        if (error.status == 403) {
          window.location.href = '/account/login'
        }
      }
    })
  }
  //-------------------------------------------------------------- //

  // ----------------- Fetch Tweets or a Single one --------------

  if (featchOneID) {
    tweetFetcher(featchOneID)
  } else {
    tweetsFetcher()
  }

  $('.addTweetForm').submit(function (event) {
    event.preventDefault()
    // const formdata = form.serialize()
    let formdata = new FormData(this);
    if (curCharsLen >= 0) {
      $.ajax({
        url: '/api/tweets/add/',
        data: formdata,
        method: 'POST',
        processData: false,
        contentType: false,
        success: function (data) {
          console.log('success')
          $('.addTweetForm').trigger("reset");
          attachTweet(data, true)
          updateHashLinks()
          $('#replyModal').modal('hide');
        },
        error: function (error) {
          console.log(error.status)
          if (error.status == 403) {
            window.location.href = '/account/login'
            console.log('hi')
          }
        }

      })
    } else {
      console.log('can\'t send your tweet too long')
      const html_ = `
      <br />
      <div class=" my-alert alert alert-warning alert-dismissible fade show" role="alert">
          can't send your tweet too long
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div> `
      const alert = $(this).find('.my-alert-div');
      alert.empty();
      alert.append(html_);
      setTimeout(() => {
        alert.empty();
      }, 5000)
    }
  })

  //---------------------------------------------------------------

  // Tweet Delete--------------------------------------------------

  $(document.body).on('submit', '#delete-tweet-form', function (event) {
    event.preventDefault();
    const form = $(this)
    const endpoint = form.attr('action')

    $.ajax({
      url: endpoint,
      method: 'DELETE',
      success: (data) => {
        tweetsContainer.html('')
        tweetsFetcher()


      },
      error: (error) => {
        if (error.status == 403) {
          window.location.href = '/account/login'
        }
        console.log(error.status)
      }
    })
  })
  //---------------------------------------------------------------
  $(document.body).on('click', '.like-btn', function (event) {
    event.preventDefault()
    let self = $(this)
    const tweetID = self.attr('data-id')
    const endpoint = '/api/tweets/' + tweetID + '/like/'
    $.ajax({
      url: endpoint,
      method: 'GET',
      success: (data) => {
        $('#likes-num-' + tweetID).text(data.likedNum)
        if (data.liked) {
          self.html('<i class="fas fa-thumbs-up"></i>')


        } else {
          self.html('<i class="far fa-thumbs-up"></i>')


        }

      },
      error: (error) => {
        console.log(error.status)
        if (error.status == 403) {
          window.location.href = '/account/login'
        }
      }
    })

  })

  $(document.body).on('click', '.reply-btn', function (event) {
    event.preventDefault()
    let self = $(this)
    const tweetID = self.attr('data-id')
    const usernameID = self.attr('data-user')
    const myInput = `
              <input type='hidden' name='parent_id' value='${tweetID}'>
              <input type='hidden' name='reply' value='true'>
                      
                      `
    $('#replyModal').modal({})
    $('#id_content2').after(myInput)
    $('#id_content2').val('Reply to @' + usernameID + ' ')
    $('#replyModal').on('shown.bs.modal', function () {
      $('#id_content2').focus();
    })

  })
  // Delete Btn //

  $(document.body).on('click', '.delete-btn', function (event) {
    const id = $(this).attr('data-id')
    const arrow = $(this).attr('data-arrow')
    html_ = ` Delete Tweet&nbsp;
              <i class="fas fa-chevron-right"></i>`
    if (arrow == 'right') {
      html_ = ` Delete Tweet&nbsp;
                <i class="fas fa-chevron-down"></i>`
      $(this).html(html_)
      $(this).attr('data-arrow', 'down')
    } else {
      $(this).html(html_)
      $(this).attr('data-arrow', 'right')
    }
    $('#delete-tweet-form-' + id).slideToggle()

  })

  //------------------------------------------------------------

  $(document.body).on('click', '.retweet-anchor', function (event) {
    event.preventDefault()
    const url_ = '/api' + $(this).attr('href')
    $.ajax({
      url: url_,
      method: 'GET',
      success: (data) => {
        attachTweet(data, true)
        updateHashLinks()
      },
      error: (error) => {
        console.log(error.status)
        if (error.status == 403) {
          window.location.href = '/account/login'
        }
      }
    })
  })

  $('#load-more-btn').click(function (e) {
    let btn = $(this);
    btn.html('Loading <i class="fas fa-spinner fa-pulse"></i>')
    tweetsFetcher(nextUrl)
  })



  // ------------- Auto Search ---------------------- //
  const doneInterval = 800;
  const searchInput = $('#search-input');
  let typingTimer;
  let searchQuery;

  searchInput.keyup(function (e) {
    searchQuery = $(this).val()
    typingTimer = setTimeout(doneSearchTyping, doneInterval)
  })
  searchInput.keydown(function (e) {
    clearTimeout(typingTimer);
  })

  function doneSearchTyping() {
    if (searchQuery) {
      const url = '/tweets/search/?q=' + searchQuery;
      document.location.href = url;
      console.log('done')
    }
  }

  // ----------------------------------------------- //

  // -------------- Chars Counter ------------------ //

  const charsLen = 255
  let curCharsLen = 0
  let spanCounter = $('.charsLeft')

  spanCounter.text(charsLen)
  $('.addTweetForm textarea').keyup(function (event) {
    curCharsLen = charsLen - $(this).val().length
    let spanID = $(this).attr('id')
    if (spanID == 'id_content2') {
      spanCounter = $('#reply-chars-counter')
    }
    spanCounter.text(curCharsLen)
    const addTweetForm = $(this).parent().parent().parent()
    if (curCharsLen > 0) {
      spanCounter.removeClass('grey-color red-color')
      addTweetForm.find('.add-tweet-btn').css({
        'opacity': '1',
      })
    } else {
      addTweetForm.find('.add-tweet-btn').css({
        'opacity': '0.5',
      })

      if (curCharsLen == 0) {
        spanCounter.addClass('grey-color')
        spanCounter.removeClass('red-color')
      } else {
        spanCounter.addClass('red-color')
        spanCounter.removeClass('grey-color')

      }
    }

  })
  // ---------------------------------------------------------
}

// Follow Btn ------------------------------------------------
$(function () {
  $('.follow-btn').on('click', function (event) {
    event.preventDefault();
    const endpoint = $(this).attr('href');
    $.ajax({
      url: endpoint,
      method: 'GET',
      success: (data) => {
        $(this).text(data.usrst)
        $('.followers-num span').text(`${data.ufn}`)

      },
      error: (error) => {
        console.log(error.status)
        if (error.status == 403) {
          window.location.href = '/account/login'
        }
      }
    })
  })

  const currenColor = $('#current-color')
  $("body").css("--main-color", currenColor.val());
  currenColor.on('change', function (event) {
    console.log($(this).val())
    $('#id_color').val($(this).val())
    $("body").css("--main-color", $(this).val());

  })



})
// ---------------------------------------------------------


