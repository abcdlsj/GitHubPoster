import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import os

def parse_activity(event_item):
    """Parse a single activity event item.
    
    Args:
        event_item: BeautifulSoup element representing an event-item div
        
    Returns:
        dict: Activity information including type, time, and details
    """
    activity = {}
    
    # Parse timestamp
    timestamp_elem = event_item.select_one('time.js-timeago')
    if timestamp_elem:
        # Convert UTC time to UTC+8
        utc_time = datetime.fromisoformat(timestamp_elem.get('datetime').replace('Z', '+00:00'))
        local_time = utc_time.astimezone(ZoneInfo('Asia/Shanghai'))
        activity['time'] = local_time.isoformat()
        
    # Parse event type
    event_type_elem = event_item.select_one('span.event-type')
    if event_type_elem:
        activity['type'] = event_type_elem.text.strip()
        
    # Parse project/repository
    project_elem = event_item.select_one('a.gl-link')
    if project_elem:
        activity['project'] = project_elem.text.strip()
        
    # Parse branch/MR details
    ref_elem = event_item.select_one('a.ref-name')
    if ref_elem:
        activity['ref'] = ref_elem.text.strip()
        
    # Parse commit details if present
    commit_elems = event_item.select('div.commit-row-title')
    if commit_elems:
        activity['commits'] = [
            {
                'sha': commit.select_one('a.commit-sha').text.strip() if commit.select_one('a.commit-sha') else '',
                'message': commit.get_text().split('·')[-1].strip() if '·' in commit.get_text() else commit.get_text().strip()
            }
            for commit in commit_elems
        ]
    
    return activity

def count_activities_from_html(content):
    """Parse activities from GitLab HTML response.
    
    Args:
        content: Can be either HTML string or JSON response with html field
        
    Returns:
        list: List of parsed activities
    """
    try:
        # Try parsing as JSON first
        if isinstance(content, str) and content.strip().startswith('{'):
            data = json.loads(content)
            if 'html' in data:
                html_content = data['html']
            else:
                html_content = content
        else:
            html_content = content

        soup = BeautifulSoup(html_content, 'html.parser')
        activities = []
        
        # Parse each event-item
        for event_item in soup.select('div.event-item'):
            activity = parse_activity(event_item)
            activities.append(activity)
            
        return activities
    except Exception as e:
        print(f"Error parsing activities: {str(e)}")
        return []

def fetch_activities(url, headers, start_offset=0, end_offset=5000, limit=100):
    """Fetch activities from GitLab API with pagination.
    
    Args:
        url: GitLab API URL
        headers: Request headers
        start_offset: Starting offset
        end_offset: Ending offset
        limit: Number of items per request
        
    Returns:
        list: All activities found
    """
    all_activities = []
    current_offset = start_offset
    
    while current_offset <= end_offset:
        try:
            params = {
                'limit': limit,
                'offset': current_offset
            }
            print(f"Fetching activities with offset {current_offset}...")
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                activities = count_activities_from_html(response.text)
                if not activities:  # If no activities found, we've reached the end
                    break
                    
                all_activities.extend(activities)
                print(f"Found {len(activities)} activities at offset {current_offset}")
            else:
                print(f"Failed to fetch data at offset {current_offset}: {response.status_code}")
                break
                
            current_offset += limit
            
        except Exception as e:
            print(f"Error at offset {current_offset}: {str(e)}")
            break
    
    return all_activities

def save_activities_to_json(activities, filename='gitlab_activities.json'):
    """Save activities to a JSON file with timestamp.
    
    Args:
        activities: List of activity dictionaries
        filename: Base filename to save to
    """
    # Add timestamp to filename
    base, ext = os.path.splitext(filename)
    timestamp = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S')
    full_filename = f"{base}_{timestamp}{ext}"
    
    # Create response structure
    response = {
        'total_count': len(activities),
        'generated_at': datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
        'timezone': 'Asia/Shanghai (UTC+8)',
        'activities': activities
    }
    
    # Save to file
    with open(full_filename, 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
    print(f"\nActivities saved to {full_filename}")
    return full_filename

def main():
    # Example usage
    gitlab_session = os.environ.get('GITLAB_SESSION')
    url = 'https://git.garena.com/users/songjian.li/activity'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Cookie': f'_gitlab_session={gitlab_session}',
        'Pragma': 'no-cache',
        'Referer': 'https://git.garena.com/users/songjian.li/activity',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    try:
        # Fetch all activities from offset 0 to 5000
        activities = fetch_activities(url, headers)
        
        print(f"\nTotal activities found: {len(activities)}")
        
        # Save activities to JSON file
        output_file = save_activities_to_json(activities)
        print(f"Activities have been saved to {output_file}")
        
        # Print summary
        print("\nActivity Summary:")
        print(f"Total activities: {len(activities)}")
        if activities:
            print(f"Date range: from {activities[-1]['time']} to {activities[0]['time']}")
            
            # Count by type
            type_counts = {}
            for activity in activities:
                activity_type = activity.get('type', 'unknown')
                type_counts[activity_type] = type_counts.get(activity_type, 0) + 1
            
            print("\nActivity types:")
            for activity_type, count in type_counts.items():
                print(f"- {activity_type}: {count}")
            
    except Exception as e:
        print(f"Error making request: {str(e)}")

if __name__ == "__main__":
    main()
