# Shared Library Version Alert Setup

This repository includes an automated system to alert teams when shared library versions are updated in the `pom.xml` file. The system is designed to ensure version alignment across all repositories.

## Overview

The system monitors changes to 7 shared libraries:
- CL_Util
- Clpss_Common
- Clpss_Occupancy
- FireRating
- CSM
- Clpss_RateCLPolicy
- Clpss_ComposePrint

## Repositories to Keep Aligned

When versions change in `cl-clpss/pom.xml`, the following repositories should be updated:
- **cl-ccl1** (pom.xml)
- **cl-jobserver** (ivy.xml)
- **cl-jobschedular** (ivy.xml)

## How It Works

1. **PR Trigger**: When a PR is opened that modifies `pom.xml`, the workflow runs
2. **Version Check**: The system compares shared library versions between the base branch and the PR branch
3. **Notifications**: If changes are detected, the system sends:
   - PR comment with detailed change information
   - Email notification to configured recipients
   - Teams notification (if configured)

## Required GitHub Secrets

To enable email notifications, add these secrets to your repository:

### Email Configuration
- `GMAIL_ID`: Gmail address for sending notifications
- `GMAIL_PASSWORD`: App-specific password for Gmail account

### Optional: Teams Integration
- `TEAMS_WEBHOOK_URL`: Microsoft Teams webhook URL for channel notifications

## Setup Instructions

### 1. Configure Gmail for Email Notifications

1. Go to your Gmail account settings
2. Enable 2-factor authentication
3. Generate an app-specific password:
   - Go to "Security" → "App passwords"
   - Generate a password for "Mail"
   - Use this password for the `GMAIL_PASSWORD` secret

### 2. Add GitHub Secrets

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following repository secrets:
   - `GMAIL_ID`: Your Gmail address
   - `GMAIL_PASSWORD`: The app-specific password from step 1

### 3. Optional: Configure Teams Notifications

1. In your Teams channel, add a "Incoming Webhook" connector
2. Copy the webhook URL
3. Add it as a repository secret named `TEAMS_WEBHOOK_URL`

## Files Overview

- `.github/workflows/shared-libs.yml`: Main workflow file
- `.github/scripts/check_version_changes.py`: Script to detect version changes
- `.github/scripts/compare_shared_lib_versions.py`: Script to compare versions across repos
- `.github/scripts/check_shared_lib_versions.py`: Legacy script for version checking

## Testing

To test the system:
1. Create a test branch
2. Modify versions of any shared library in `pom.xml`
3. Open a PR
4. The workflow should trigger and send notifications

## Customization

### Adding More Libraries
Edit the `SHARED_LIBRARIES` list in the Python scripts to include additional libraries.

### Changing Notification Recipients
Update the `to` field in the email notification step in the workflow file.

### Modifying Notification Content
Edit the message templates in `check_version_changes.py`.

## Troubleshooting

### Email Not Sending
- Verify Gmail secrets are correct
- Check that 2FA is enabled on Gmail account
- Ensure app-specific password is used (not regular password)

### Teams Notification Not Working
- Verify webhook URL is correct
- Check that the Teams channel has the Incoming Webhook connector configured

### Workflow Not Triggering
- Ensure changes are made to `pom.xml` file
- Check that the workflow file is in the correct location
- Verify branch permissions and PR requirements

## Support

For issues with the notification system, check:
1. GitHub Actions logs for error details
2. Repository secrets configuration
3. Email and Teams integration settings
