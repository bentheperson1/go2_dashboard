
#Topics only available through WebRTC (however will work through DDS)

WEBRTC_TOPICS = [
    # General Device Control and Configuration
    "rt/rtc_status",
    "rt/rtc/state",
    "rt/servicestate",
    "rt/servicestateactivate",
    "rt/public_network_status",

    # API Requests and Responses
    "rt/videohub/inner",
    "rt/api/videohub/request",
    "rt/api/videohub/response",
    "rt/api/uwbswitch/request",
    "rt/api/uwbswitch/response",
    "rt/api/bashrunner/request",
    "rt/api/bashrunner/response",
    "rt/api/obstacles_avoid/request",
    "rt/api/obstacles_avoid/response",
    "rt/api/vui/request",
    "rt/api/vui/response",
    "rt/api/gpt/request",
    "rt/api/gpt/response",
    "rt/api/sport/request",
    "rt/api/sport/response",
    "rt/api/robot_state/request",
    "rt/api/robot_state/response",
    "rt/api/audiohub/request",
    "rt/api/audiohub/response",
    "rt/api/config/request",
    "rt/api/config/response",
    "rt/api/motion_switcher/request",
    "rt/api/motion_switcher/response",
    "rt/api/gas_sensor/request",
    "rt/api/gas_sensor/response",

    # SLAM and Mapping
    "rt/qt_command",
    "rt/qt_add_node",
    "rt/qt_add_edge",
    "rt/qt_notice",
    "rt/pctoimage_local",
    "rt/lio_sam_ros2/mapping/odometry",

    # Query and Feedback
    "rt/query_result_node",
    "rt/query_result_edge",
    "rt/gptflowfeedback",

    # Sensor Data
    "rt/utlidar/switch",
    "rt/utlidar/voxel_map_compressed",
    "rt/utlidar/lidar_state",
    "rt/utlidar/robot_pose",
    "rt/uwbstate",

    # Device State
    "rt/multiplestate",
    "rt/lf/lowstate",
    "rt/lf/sportmodestate",
    "rt/audiohub/player/state",
    "rt/selftest",
    "rt/gas_sensor",

    # Arm Commands and Feedback
    "rt/arm_Command",
    "rt/arm_Feedback",

    # Wireless Controller
    "rt/wirelesscontroller",
]


DDS_ONLY_TOPICS = [
    "rt/sportmodestate",
    "rt/mf/sportmodestate",
    "rt/utlidar/voxel_map",
    "rt/lowstate",
    "rt/lowcmd"
]

# Combine WebRTC topics with DDS-specific topics for comprehensive DDS topics
DDS_TOPICS = WEBRTC_TOPICS + DDS_ONLY_TOPICS
