import vk
import time
from vk_data import VKData

class Connection:
    def __init__(self, app_id, login, password):
        """
        Creates new session and api objects
        Logs processing
        """
        print('Connecting...')
        self.app_id = app_id
        self.login = login
        self.password = password

        print('Create session...')
        self.session = vk.AuthSession(app_id=VKData.APP_ID, \
            user_login=VKData.LOGIN, user_password=VKData.PASSWORD)
        print('Completed!')
        print('----------')

        print('Create API...')        
        self.vkAPI = vk.API(self.session)
        print('Completed!')
        print('----------')
        

    def get_groups_amount(self, id_user):
        """
        Returns the number of groups of user with ID = id_user
        Logs processing
        """
        print('Get and count groups...')
        groups = self.vkAPI.groups.get(user_id=id_user)
        print('Completed!')
        print('----------')
        
        return len(groups)

    def get_groups_names(self, id_user):
        """
        Returns list with the names of groups of user with ID = id_user
        Logs processing
        """
        print('Get groups...')
        groups = self.vkAPI.groups.get(user_id=id_user, extended=1)
        print('Get names of groups...')
        names = [group['screen_name'] for group in groups[1:]]
        print('Completed!')
        print('----------')
        
        return names

    def get_groups_extended(self, id_user):
        """
        Returns list with extended information about groups of user with ID = id_user
        Logs processing
        """
        print('Get groups...')
        groups = self.vkAPI.groups.get(user_id=id_user, extended=1)
        print('Completed!')
        print('----------')
        
        return groups

    def get_groups_id(self, id_user):
        """
        Returns list of groups id of user with ID = id_user
        """
        groups = self.vkAPI.groups.get(user_id=id_user)
        return groups

    def get_likes_in_groups(self, id_user, count_posts):
        """
        Returns links to posts liked by user with ID = id_user from his groups 
        Checks last "count_posts" posts in each group
        Logs processing
        """
        print('Start processing...')
        likes = []
        print('Get id of groups...')
        ids = self.get_groups_id(id_user)
        print('Completed!')

        print('Get names of groups...')
        names = self.get_groups_names(id_user)
        print('Completed!')
        
        for i in range(len(ids)):
            # Sleep to avoid VkAPIError: Too many requests per second
            time.sleep(0.3)
            # Get last "count_posts" posts from another group
            try:
                wall = self.vkAPI.wall.get(owner_id='-'+str(ids[i]), count=count_posts)
                print('Check ' + names[i] + '...')
            except:
                continue
    
            for wall_post in wall[1:]:
                time.sleep(0.3)
                isLiked = self.vkAPI.likes.isLiked(user_id=id_user, \
                    type='post', owner_id='-'+str(ids[i]), item_id=wall_post['id'])
                
                if (isLiked):
                    tmp = 'https://vk.com/' + names[i] + '?' + \
                        'w=wall-' + str(ids[i]) + '_' + str(wall_post['id'])
                                                 
                    print(tmp)
                    likes.append(tmp)
                    
            print('Check completed!')
            print('----------')
                                                                                                   
        return likes

    def get_likes_from_user(self, id_user, count_posts):
        """
        Returns dict with id of friends(key) and amount of likes(value)
        Logs processing
        """
        print('Start processing...')
        likes = {}
        print('Get id of friends...')
        ids = self.get_friends_id(id_user)
        print('Completed!')
        
        for i in range(len(ids)):
            time.sleep(0.3)
            try:
                wall = self.vkAPI.wall.get(owner_id=str(ids[i]), count=count_posts)
                print('Check https://vk.com/id' + str(ids[i]))
            except:
                continue

            index = 0
            for wall_post in wall[1:]:
                
                time.sleep(0.3)
                isLiked = self.vkAPI.likes.isLiked(user_id=id_user, \
                    type='post', owner_id=str(ids[i]), item_id=wall_post['id'])
                
                if (isLiked):
                    index+=1
               
            print('Check completed!')
            print('Likes: ' + str(index))
            print('----------')
            key = 'https://vk.com/id' + str(ids[i]);
            likes[key] = index
                                                                                                   
        return likes

    
    def get_friends_id(self, id_user):
        """
        Returns list of id of friends of user with ID = id_user
        """
        friends = self.vkAPI.friends.get(user_id=id_user, order='random')
        return friends

    def get_friends_amount(self, id_user):
        """
        Returns amount of friends of user with ID = id_user
        """
        friends = self.vkAPI.friends.get(user_id=id_user)
        return len(friends)
        
    
