# Copyright 2021 Tier IV, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for the `SetVehicleInfo` action."""

from typing import Union

from launch import Action
from launch.frontend import Entity
from launch.frontend import expose_action
from launch.frontend import Parser
from launch.launch_context import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.utilities.typing_file_path import FilePath

from launch_ros.parameters_type import ParameterFile

import yaml


@expose_action('set_vehicle_info')
class SetVehicleInfo(Action):
    """Action that sets a vehicle info parameter from file."""

    def __init__(
        self,
        param_file: Union[FilePath, SomeSubstitutionsType],
        **kwargs
    ) -> None:
        """Create a SetVehicleInfo action."""
        super().__init__(**kwargs)
        self.__param_file = ParameterFile(param_file)

    @classmethod
    def parse(cls, entity: Entity, parser: Parser):
        """Return `SetVehicleInfo` action and kwargs for constructing it."""
        _, kwargs = super().parse(entity, parser)
        kwargs['param_file'] = parser.parse_substitution(entity.get_attr('param_file'))
        return cls, kwargs

    @property
    def param_file(self) -> ParameterFile:
        """Getter for param file."""
        return self.__param_file

    def execute(self, context: LaunchContext):
        """Execute the action."""
        with open(str(self.__param_file.evaluate(context)), 'r') as f:
            eval_param_dict = yaml.safe_load(f)['/**']['ros__parameters']

        vehicle_info_keys = {'wheel_radius', 'wheel_width', 'wheel_base',
                             'wheel_tread', 'front_overhang', 'rear_overhang',
                             'left_overhang', 'right_overhang', 'vehicle_height'}

        if vehicle_info_keys <= eval_param_dict.keys():
            eval_param_dict['ready_vehicle_info_param'] = True
            global_params = context.launch_configurations.get('ros_params', {})
            global_params.update(eval_param_dict)
            context.launch_configurations['ros_params'] = global_params
        else:
            raise RuntimeError('vehicle info param file is invalid.')
