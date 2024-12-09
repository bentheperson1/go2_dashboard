from typing import Type, cast, Any
import importlib

import cyclonedds.idl._type_helper as _th

import dataclasses
import typing
import logging


class IDLDataClass:
    _data_class_cache = {}
    _path = 'unitree_sdk2py.idl'

    unitree_api = {
        'Request_': f'{_path}.unitree_api.msg.dds_',
        'RequestHeader_': f'{_path}.unitree_api.msg.dds_',
        'RequestIdentity_': f'{_path}.unitree_api.msg.dds_',
        'RequestLease_': f'{_path}.unitree_api.msg.dds_',
        'RequestPolicy_': f'{_path}.unitree_api.msg.dds_',
        'Response_': f'{_path}.unitree_api.msg.dds_',
        'ResponseHeader_': f'{_path}.unitree_api.msg.dds_',
        'ResponseStatus_': f'{_path}.unitree_api.msg.dds_',
    }

  
    unitree_go = {
        'AudioData_': f'{_path}.unitree_go.msg.dds_',
        'BmsCmd_': f'{_path}.unitree_go.msg.dds_',
        'BmsState_': f'{_path}.unitree_go.msg.dds_',
        'Error_': f'{_path}.unitree_go.msg.dds_',
        'Go2FrontVideoData_': f'{_path}.unitree_go.msg.dds_',
        'HeightMap_': f'{_path}.unitree_go.msg.dds_',
        'IMUState_': f'{_path}.unitree_go.msg.dds_',
        'InterfaceConfig_': f'{_path}.unitree_go.msg.dds_',
        'LidarState_': f'{_path}.unitree_go.msg.dds_',
        'LowCmd_': f'{_path}.unitree_go.msg.dds_',
        'LowState_': f'{_path}.unitree_go.msg.dds_',
        'MotorCmd_': f'{_path}.unitree_go.msg.dds_',
        'MotorState_': f'{_path}.unitree_go.msg.dds_',
        'PathPoint_': f'{_path}.unitree_go.msg.dds_',
        'Req_': f'{_path}.unitree_go.msg.dds_',
        'Res_': f'{_path}.unitree_go.msg.dds_',
        'SportModeCmd_': f'{_path}.unitree_go.msg.dds_',
        'SportModeState_': f'{_path}.unitree_go.msg.dds_',
        'TimeSpec_': f'{_path}.unitree_go.msg.dds_',
        'UwbState_': f'{_path}.unitree_go.msg.dds_',
        'UwbSwitch_': f'{_path}.unitree_go.msg.dds_',
        'WirelessController_': f'{_path}.unitree_go.msg.dds_',
    }


    std_msgs = {
        'Header_': f'{_path}.std_msgs.msg.dds_',
        'String_': f'{_path}.std_msgs.msg.dds_',
    }

   
    geometry_msgs = {
        'Point32_': f'{_path}.geometry_msgs.msg.dds_',
        'Point_': f'{_path}.geometry_msgs.msg.dds_',
        'PointStamped_': f'{_path}.geometry_msgs.msg.dds_',
        'Pose2D_': f'{_path}.geometry_msgs.msg.dds_',
        'Pose_': f'{_path}.geometry_msgs.msg.dds_',
        'PoseStamped_': f'{_path}.geometry_msgs.msg.dds_',
        'PoseWithCovariance_': f'{_path}.geometry_msgs.msg.dds_',
        'PoseWithCovarianceStamped_': f'{_path}.geometry_msgs.msg.dds_',
        'Quaternion_': f'{_path}.geometry_msgs.msg.dds_',
        'QuaternionStamped_': f'{_path}.geometry_msgs.msg.dds_',
        'Twist_': f'{_path}.geometry_msgs.msg.dds_',
        'TwistStamped_': f'{_path}.geometry_msgs.msg.dds_',
        'TwistWithCovariance_': f'{_path}.geometry_msgs.msg.dds_',
        'TwistWithCovarianceStamped_': f'{_path}.geometry_msgs.msg.dds_',
        'Vector3_': f'{_path}.geometry_msgs.msg.dds_',
    }

    builtin_interfaces = {
        'Time_': f'{_path}.builtin_interfaces.msg.dds_',
    }

    nav_msgs = {
        'MapMetaData_': f'{_path}.nav_msgs.msg.dds_',
        'OccupancyGrid_': f'{_path}.nav_msgs.msg.dds_',
        'Odometry_': f'{_path}.nav_msgs.msg.dds_',
    }
    
    sensor_msgs = {
        'PointCloud2_': f'{_path}.sensor_msgs.msg.dds_',
        'PointField_': f'{_path}.sensor_msgs.msg.dds_',
    }

    @classmethod
    def get_package_path(cls, class_name):
        for category in [cls.unitree_api, cls.unitree_go, cls.std_msgs, cls.geometry_msgs, cls.builtin_interfaces, cls.nav_msgs, cls.sensor_msgs]:
            if class_name in category:
                return category[class_name]
        return None

    @classmethod
    def get_data_class(cls, class_name):
        """
        Dynamically imports and returns a data class based on its name.
        """
        if class_name in cls._data_class_cache:
            return cls._data_class_cache[class_name]

        module_name = cls.get_package_path(class_name)
        if not module_name:
            raise ImportError(f"No module found for class {class_name}")

        module = importlib.import_module(module_name)
        data_class = getattr(module, class_name, None)
        if not data_class:
            raise ImportError(f"Class {class_name} not found in module {module_name}")

        cls._data_class_cache[class_name] = data_class
        return cast(Type[Any], data_class)

    
    
    def create_zeroed_dataclass(self, cls: type) -> any:
        """Create an instance of a dataclass with all fields set to default 'zero' values based on their type."""
        field_defaults = {}
        for field in dataclasses.fields(cls):
            field_type = field.type

            # Get the base type and annotations if it's an annotated type
            if _th.get_origin(field_type) is _th.Annotated:
                base_type, *annotations = _th.get_args(field_type)
                custom_type = annotations[0] if annotations else base_type
            else:
                base_type, custom_type = field_type, field_type

            # Debugging
            # print(f"Zero out Field: {field.name}, Base type: {base_type}, Custom type: {custom_type}, misc: {base_type}")

            #check if the field is array
            if base_type is int:
                default_value = 0
            elif base_type is float:
                default_value = 0.0
            elif isinstance(base_type, str):
                #Check if we have dataclass instance, Idn why the dataclass name goes as a string, a bit confusing 
                dataclass_name = base_type.rsplit('.', 1)[-1]
                dataclass_factory = self.get_data_class(dataclass_name)
                default_value = self.create_zeroed_dataclass(dataclass_factory)

            elif issubclass(_th.get_origin(base_type), typing.Sequence):
                
                custom_element_subtype = custom_type.subtype
                custom_element_length = custom_type.length
                element_type = _th.get_args(base_type)[0]

                if _th.get_origin(element_type) is _th.Annotated:
                    element_type = _th.get_args(element_type)[0]

                # print (f"ARRAY: element_type: {element_type}, length: {custom_element_length}")

                if element_type is int:
                    element_default = [0 for _ in range(custom_element_length)]
                    default_value = element_default
                elif element_type is float:
                    element_default = [0.0 for _ in range(custom_element_length)]
                    default_value = element_default
                elif isinstance(base_type, str):
                    element_default = ["" for _ in range(custom_element_length)]
                    default_value = element_default

                #this part will recursively zero out the included dataclasses
                elif isinstance(element_type, typing.ForwardRef):
                    print(type(custom_element_subtype))
                    # dataclass_name = custom_element_subtype.rsplit('.', 1)[-1]
                    # dataclass_factory = self.get_data_class(dataclass_name)
                    dataclass_factory = custom_element_subtype
                    default_value = [self.create_zeroed_dataclass(dataclass_factory) for _ in range(custom_element_length)]
            else:
                default_value= None

            field_defaults[field.name] = default_value

        return cls(**field_defaults)
    

