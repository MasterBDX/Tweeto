from accounts.forms import UserProfileColorForm


def color_object(request):
    form = UserProfileColorForm()
    try:
        color = request.user.profile.color
    except:
        color = None
    if not color:
        color = '#2ecc71'
    return {'color': color, 'color_form': form}
